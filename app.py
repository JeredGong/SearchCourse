from flask import Flask, request, jsonify, send_from_directory, render_template
import pandas as pd
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # 允许跨域请求

# 读取课程数据
df = pd.read_csv('Courses.csv', encoding='gbk')

@app.route('/')
def serve_index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/search', methods=['GET'])
def search():
    course_name = request.args.get('course_name', '')
    instructor = request.args.get('instructor', '')
    query = df.copy()

    # 处理NaN值，填充为"未知"
    query = query.fillna('未知')

    print(f"Received search parameters: course_name={course_name}, instructor={instructor}")

    if course_name:
        query = query[query['课程名称'].str.contains(course_name, na=False)]
    if instructor:
        query = query[query['授课老师'].str.contains(instructor, na=False)]

    results = query.to_dict(orient='records')

    print(f"Query results: {results}")

    # 调试输出JSON响应
    json_results = json.dumps(results, ensure_ascii=False)
    print(f"JSON results: {json_results}")

    response = jsonify(results)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/add_course', methods=['POST'])
def add_course():
    new_course = request.json
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
        print(f"Error adding course: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
