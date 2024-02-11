document.addEventListener("DOMContentLoaded", () => {
    const submitForm = document.getElementById("submit_form");
    const classResults = document.getElementById("class-results");

    submitForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const name = document.getElementById("name").value;
        const score = parseInt(document.getElementById("score").value);

        fetch("/submit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name, score }),
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error("서버 응답 오류 발생");
            }
            return response.json();
        })
        .then((data) => {
            // 반 배정 결과 출력
            classResults.innerHTML = '';
            data.classes.forEach((classStudents, index) => {
                const classHeading = document.createElement('h2');
                classHeading.textContent = `${index + 1}반`;
                classResults.appendChild(classHeading);

                const classList = document.createElement('ul');
                classStudents.forEach((student) => {
                    const studentItem = document.createElement('li');
                    studentItem.textContent = `${student[0]} (${student[2]}등)`;
                    classList.appendChild(studentItem);
                });

                classResults.appendChild(classList);
            });
        })
        .catch((error) => {
            // 오류 처리
            console.error("오류 발생:", error.message);
            // 여기에 오류 처리 코드를 작성할 수 있습니다.
        });
    });
});
