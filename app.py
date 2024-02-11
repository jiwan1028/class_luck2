from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# 반의 개수
num_classes = 6

# 학생 정보 리스트 (이름, 점수, 등수)
students = []


@app.route("/")
def index():
    """
    메인 페이지
    """
    return render_template("index.html", classes=[])


@app.route("/submit", methods=["POST"])
def submit():
    """
    정보 제출 및 반 배정 결과 출력
    """
    data = request.json

    # 이름과 점수를 추출합니다.
    name = data.get("name")
    score = data.get("score")

    # 데이터 유효성 검사
    if not name or not score:
        return jsonify({"error": "이름과 점수를 입력하세요."}), 400

    try:
        score = int(score)
    except ValueError:
        return jsonify({"error": "점수는 숫자 형식이어야 합니다."}), 400

    # 학생 정보 추가
    students.append((name, score, len(students) + 1))

    # 점수순으로 정렬
    students.sort(key=lambda x: x[1], reverse=True)

    # 등수 계산
    for i in range(len(students)):
        students[i] = (students[i][0], students[i][1], i + 1)

    # 각 반에 배정될 학생들의 리스트
    classes = [[] for _ in range(num_classes)]

    # 반 배정
    for i in range(len(students)):
        # 학생의 등수
        rank = students[i][2]

        # 배정될 반
        class_num = (rank - 1) % num_classes

        # 학생 배정
        classes[class_num].append(students[i])

    return jsonify({"classes": classes}), 200


if __name__ == "__main__":
    app.run(debug=True)
