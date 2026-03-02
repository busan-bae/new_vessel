// 플래시 메시지 자동 숨김 처리
// DOMContentLoaded: HTML이 완전히 로드된 후 실행
document.addEventListener('DOMContentLoaded', () => {
  const flashes = document.querySelectorAll('.flash');

  flashes.forEach(flash => {
    // 3초 후 페이드 아웃
    setTimeout(() => {
      flash.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      flash.style.opacity = '0';
      flash.style.transform = 'translateY(-8px)';

      // 애니메이션 끝난 후 DOM에서 제거
      setTimeout(() => flash.remove(), 400);
    }, 3000);
  });
});
