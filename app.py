from flask import Flask, request, jsonify, send_from_directory, render_template, make_response
import pandas as pd
from flask_cors import CORS
import orjson
import gzip
import redis
from datetime import datetime, timedelta
import threading
import time
from functools import lru_cache

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)
# 初始化Redis连接池
pool = redis.ConnectionPool(host='localhost', port=6379, db=0, max_connections=10)
cache = redis.Redis(connection_pool=pool)

# 读取课程数据并缓存到内存中
df = pd.read_csv('CouresesData.csv', encoding='gbk').fillna('未知')

# 使用字典作为内存缓存，用于存储独立IP的访问量
ip_cache = set()
cache_lock = threading.Lock()

def reset_ip_cache():
    """每天北京时间0点重置缓存"""
    while True:
        now = datetime.now()
        # 计算下一次北京时间0点的时间
        next_reset_time = (datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        sleep_seconds = (next_reset_time - now).total_seconds()

        if app.debug:
            print(f"Scheduled cache reset at {next_reset_time} (in {sleep_seconds} seconds)")

        # 休眠直到下一次清理
        time.sleep(sleep_seconds)

        # 清空缓存
        with cache_lock:
            ip_cache.clear()
            if app.debug:
                print(f"Cache reset at {datetime.now()}")

# 启动缓存清理线程
threading.Thread(target=reset_ip_cache, daemon=True).start()

def record_ip(client_ip):
    """记录客户端IP地址"""
    with cache_lock:
        ip_cache.add(client_ip)

@lru_cache(maxsize=32)
def search_cache(course_name, instructor):
    """内存缓存，用于缓存高频搜索查询"""
    query = df.copy()
    if course_name:
        query = query[query['课程名称'].str.contains(course_name, na=False)]
    if instructor:
        query = query[query['授课老师'].str.contains(instructor, na=False)]

    results = query.to_dict(orient='records')
    return results

@app.route('/')
def serve_index():
    # 获取客户端IP地址
    client_ip = request.remote_addr

    # 异步记录IP
    threading.Thread(target=record_ip, args=(client_ip,)).start()

    # 设置浏览器缓存首页内容（例如缓存1小时）
    response = make_response(render_template('index.html'))
    response.headers['Cache-Control'] = 'public, max-age=3600'
    return response


@app.route('/static/<path:path>')
def serve_static(path):
    # 设置缓存头，让静态文件在浏览器中缓存（例如缓存30天）
    response = send_from_directory('static', path)
    response.headers['Cache-Control'] = 'public, max-age=2592000'
    return response


@app.route('/search', methods=['GET'])
def search():
    course_name = request.args.get('course_name', '')
    instructor = request.args.get('instructor', '')

    # 创建缓存键
    cache_key = f"search:{course_name}:{instructor}"
    cached_results = cache.get(cache_key)

    if cached_results:
        results = orjson.loads(cached_results)
    else:
        # 优先使用内存缓存
        results = search_cache(course_name, instructor)

        # 缓存查询结果到Redis中，缓存6小时
        cache.set(cache_key, orjson.dumps(results), ex=6 * 60 * 60)

    # 压缩响应数据
    response = app.response_class(
        response=gzip.compress(orjson.dumps(results)),
        status=200,
        mimetype='application/json'
    )
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['Cache-Control'] = 'public, max-age=3600'  # 缓存1小时
    return response


@app.route('/statistic', methods=['GET'])
def get_statistics():
    try:
        courses_count = len(df)
        try:
            new_courses_df = pd.read_csv('NewCourses.csv', encoding='gbk')
            new_courses_count = len(new_courses_df)
        except FileNotFoundError:
            new_courses_count = 0
        evaluation_count = courses_count + new_courses_count

        # 获取当前缓存中的IP访问数量
        visit_count = len(ip_cache)

        response_data = {
            'evaluationCount': evaluation_count,
            'visitCount': visit_count
        }

        # 压缩响应数据
        response = app.response_class(
            response=gzip.compress(orjson.dumps(response_data)),
            status=200,
            mimetype='application/json'
        )
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    except Exception as e:
        if app.debug:
            print(f"Error fetching statistics: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
