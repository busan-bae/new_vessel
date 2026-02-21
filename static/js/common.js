setTimeout(function() {
    let messages = document.querySelectorAll('.flash-message');
    messages.forEach(function(message) {
        message.classList.add('flash-hide');           // 퇴장 애니메이션 실행
        setTimeout(function() {
            message.style.display = 'none';   // 완전히 사라짐
        },400)
    })
},3000);

const deleteForms = document.querySelector('#delete-form');
if (deleteForms) {// 삭제 폼이 있는 페이지 에서만 실행
    deleteForms.addEventListener('submit', function(event) {
        const confirmed = confirm('정말 삭제하시겠습니까?');
        if (!confirmed) {
            event.preventDefault(); // 폼 제출 취소
        }
    });
}