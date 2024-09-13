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
app.config['USE_ETAGS'] = True  # 启用 ETag 缓存
CORS(app)
# 初始化Redis连接池
pool = redis.ConnectionPool(host='localhost', port=6379, db=0, max_connections=10)
cache = redis.Redis(connection_pool=pool)

# 读取课程数据并缓存到内存中
df = pd.read_csv('CouresesData.csv', encoding='gbk').fillna('未知')

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
    # 设置浏览器缓存首页内容（例如缓存1小时）
    response = make_response(render_template('index.html'))
    response.headers['Cache-Control'] = 'public, max-age=360000'
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
        cache.set(cache_key, orjson.dumps(results), ex=24 * 60 * 60)

    # 压缩响应数据
    response = app.response_class(
        response=gzip.compress(orjson.dumps(results)),
        status=200,
        mimetype='application/json'
    )
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['Cache-Control'] = 'public, max-age=7200'  # 缓存1小时
    return response

def validate_course_data(course_data):
    required_fields = ['course_name', 'course_attribute', 'instructor', 'content', 'attendance', 'assessment', 'grade']
    for field in required_fields:
        if field not in course_data:
            return False, f"Missing required field: {field}"

    if course_data['grade'] != 'Unknown':
        try:
            grade = int(course_data['grade'])
            if grade < 0 or grade > 100:
                return False, "Grade must be between 0 and 100 or 'Unknown'"
        except ValueError:
            return False, "Grade must be an integer between 0 and 100 or 'Unknown'"

    return True, None
@app.route('/add_course', methods=['POST'])
def add_course():
    new_course = request.json
    is_valid, error_message = validate_course_data(new_course)
    if not is_valid:
        return jsonify({'error': error_message}), 400

    try:
        # 将新课程评价添加到新的 DataFrame
        new_course_df = pd.DataFrame([new_course])

        # 尝试读取现有的 NewCourses.csv 文件，如果不存在则创建新的
        try:
            existing_df = pd.read_csv('NewCourses.csv', encoding='gbk')
            updated_df = pd.concat([existing_df, new_course_df], ignore_index=True)
        except FileNotFoundError:
            updated_df = new_course_df

        # 将更新后的 DataFrame 写入 NewCourses.csv 文件
        updated_df.to_csv('NewCourses.csv', encoding='gbk', index=False)

        return jsonify({'message': 'Course added successfully'}), 200
    except Exception as e:
        if app.debug:
            print(f"Error adding course: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/add_survey', methods=['POST'])
def add_survey():
    survey_data = request.json

    # 定义必填字段
    required_fields = ['curricula', 'suggestions', 'accept', 'expectation', 'timestamp']

    # 验证数据完整性
    for field in required_fields:
        if field not in survey_data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    try:
        # 将问卷数据添加到新的 DataFrame
        new_survey_df = pd.DataFrame([survey_data])

        # 尝试读取现有的 surveyData.csv 文件，如果不存在则创建新的
        try:
            existing_survey_df = pd.read_csv('surveyData.csv', encoding='utf-8')
            updated_survey_df = pd.concat([existing_survey_df, new_survey_df], ignore_index=True)
        except FileNotFoundError:
            updated_survey_df = new_survey_df

        # 将更新后的 DataFrame 写入 surveyData.csv 文件
        updated_survey_df.to_csv('surveyData.csv', encoding='utf-8', index=False)

        return jsonify({'message': 'Survey submitted successfully'}), 200
    except Exception as e:
        if app.debug:
            print(f"Error adding survey: {e}")
        return jsonify({'error': str(e)}), 500
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
        visit_count = new_courses_count

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
