function animateStars(count) {
    const starsDiv = document.querySelector(".stars");
    starsDiv.innerHTML = "";
  
    for (let i = 0; i < count; i++) {
      const star = document.createElement("span");
      star.classList.add("star");
      star.textContent = "★";
      star.style.animationDelay = `${i * 0.1}s`;
      starsDiv.appendChild(star);
    }
  
    if (count === 0) {
      starsDiv.innerHTML = "<span class='star' style='color: red;'>💀</span> <p style='margin-top: 10px;'>Disgusting product!</p>";
    }
  }
  