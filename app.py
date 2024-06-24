from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import pandas as pd
import json

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)



# 读取课程数据
df = pd.read_csv('CouresesData.csv', encoding='gbk')

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

    if app.debug:
        print(f"Received search parameters: course_name={course_name}, instructor={instructor}")

    if course_name:
        query = query[query['课程名称'].str.contains(course_name, na=False)]
    if instructor:
        query = query[query['授课老师'].str.contains(instructor, na=False)]

    results = query.to_dict(orient='records')

    if app.debug:
        print(f"Query results: {results}")

    # 调试输出JSON响应
    if app.debug:
        json_results = json.dumps(results, ensure_ascii=False)
        print(f"JSON results: {json_results}")

    response = jsonify(results)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
