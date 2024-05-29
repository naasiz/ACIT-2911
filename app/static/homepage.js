  //Comment
  function showComment(){
    var commentArea = document.getElementById("comment-area");
    commentArea.classList.remove("hide");
  }
  
  //Reply
  function showReply(){
    var replyArea = document.getElementById("reply-area");
    replyArea.classList.remove("hide");
  }
// navbar
function toggleNavbar() {
  const navbarBurger = document.querySelector('.navbar-burger');
  const navbarMenu = document.getElementById(navbarBurger.dataset.target);
  navbarBurger.classList.toggle('is-active');
  navbarMenu.classList.toggle('is-active');
}
// src = https://codepen.io/MinzCode/pen/qBqrMMP

let canvas, ctx, w, h, stars = [], meteors = [];

function init() {
	canvas = document.querySelector(".Star-background #canvas");
	ctx = canvas.getContext("2d");
	resizeReset();
	for (let a = 0; a < w * h * 0.0001; a++) {
		stars.push(new Star());
	}
	for (let b = 0; b < 2; b++) {
		meteors.push(new Meteor());
	}
	animationLoop();
}

function resizeReset() {
	w = canvas.width = window.innerWidth;
	h = canvas.height = window.innerHeight;
}

function animationLoop() {
	ctx.clearRect(0, 0, w, h);
	drawScene();
	requestAnimationFrame(animationLoop);
}

function drawScene() {
	stars.map((star) => {
		star.update();
		star.draw();
	});
	meteors.map((meteor) => {
		meteor.update();
		meteor.draw();
	});
}


class Star {
	constructor() {
		this.x = Math.random() * w;
		this.y = Math.random() * h;
		this.size = Math.random() + 0.5;
		this.blinkChance = 0.005;
		this.alpha = 1;
		this.alphaChange = 0;
	}
	draw() {
		ctx.beginPath();
		ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
		ctx.fillStyle = `rgba(255, 255, 255, ${this.alpha})`;
		ctx.fill();
		ctx.closePath();
	}
	update() {
		if (this.alphaChange === 0 && Math.random() < this.blinkChance) {
			this.alphaChange = -1;
		} else if (this.alphaChange !== 0) {
			this.alpha += this.alphaChange * 0.05;
			if (this.alpha <= 0) {
				this.alphaChange = 1;
			} else if (this.alpha >= 1) {
				this.alphaChange = 0;
			}
		}
	}
}

class Meteor {
	constructor() {
		this.reset();
	}
	reset() {
		this.x = Math.random() * w + 300; 
		this.y = -100;
		this.size = Math.random() * 2 + 0.5;
		this.speed = (Math.random() + 0.5) * 15;
	}
	draw() {
		ctx.save();
		ctx.strokeStyle = "rgba(255, 255, 255, .1)";
		ctx.lineCap = "round";
		ctx.shadowColor = "rgba(255, 255, 255, 1)";
		ctx.shadowBlur = 10;
		for (let i = 0; i < 10; i++) {
			ctx.beginPath();
			ctx.moveTo(this.x, this.y);
			ctx.lineWidth = this.size;
			ctx.lineTo(this.x + 10 * (i + 1), this.y - 10 * (i + 1));
			ctx.stroke();
			ctx.closePath();
		}
		ctx.restore();
	}
	update() {
		this.x -= this.speed;
		this.y += this.speed;
		if (this.y >= h + 100) {
			this.reset();
		}
	}
}

window.addEventListener("DOMContentLoaded", init);
window.addEventListener("resize", resizeReset);