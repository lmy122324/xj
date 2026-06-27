// Carousel
(function(){
  const carousel = document.querySelector('.carousel');
  if(!carousel) return;
  const slides = carousel.querySelector('.carousel-slides');
  const dots = carousel.querySelectorAll('.carousel-dot');
  const prev = carousel.querySelector('.prev');
  const next = carousel.querySelector('.next');
  let current = 0;
  const total = dots.length;

  function goTo(i){
    current = ((i % total) + total) % total;
    slides.style.transform = `translateX(-${current * 100}%)`;
    dots.forEach((d, j) => d.classList.toggle('active', j === current));
  }

  prev.addEventListener('click', () => goTo(current - 1));
  next.addEventListener('click', () => goTo(current + 1));
  dots.forEach((d, i) => d.addEventListener('click', () => goTo(i)));

  setInterval(() => goTo(current + 1), 5000);
})();

// Login form
(function(){
  const loginForm = document.getElementById('login-form');
  if(!loginForm) return;
  loginForm.addEventListener('submit', function(e){
    e.preventDefault();
    var u = document.getElementById('username').value.trim();
    var p = document.getElementById('password').value.trim();
    var msg = document.getElementById('message');
    if(!u || !p){ msg.textContent = '请填写完整信息'; msg.style.color='#e74c3c'; return; }
    var users = JSON.parse(localStorage.getItem('travel_users') || '[]');
    var user = users.find(function(x){ return x.username === u && x.password === p; });
    if(user){
      msg.textContent = '登录成功！正在跳转...';
      msg.style.color = '#2EC4B6';
      localStorage.setItem('travel_current_user', JSON.stringify(user));
      setTimeout(function(){ window.location.href = 'index.html'; }, 1000);
    } else {
      msg.textContent = '用户名或密码错误';
      msg.style.color = '#e74c3c';
    }
  });
})();

// Register form
(function(){
  const regForm = document.getElementById('register-form');
  if(!regForm) return;
  regForm.addEventListener('submit', function(e){
    e.preventDefault();
    var u = document.getElementById('reg-username').value.trim();
    var p = document.getElementById('reg-password').value.trim();
    var p2 = document.getElementById('reg-password2').value.trim();
    var n = document.getElementById('reg-name').value.trim();
    var msg = document.getElementById('message');
    if(!u || !p || !p2 || !n){ msg.textContent = '请填写完整信息'; msg.style.color='#e74c3c'; return; }
    if(p !== p2){ msg.textContent = '两次密码不一致'; msg.style.color='#e74c3c'; return; }
    if(p.length < 6){ msg.textContent = '密码至少6位'; msg.style.color='#e74c3c'; return; }
    var users = JSON.parse(localStorage.getItem('travel_users') || '[]');
    if(users.find(function(x){ return x.username === u; })){
      msg.textContent = '用户名已存在';
      msg.style.color = '#e74c3c';
      return;
    }
    users.push({username: u, password: p, name: n});
    localStorage.setItem('travel_users', JSON.stringify(users));
    msg.textContent = '注册成功！';
    msg.style.color = '#2EC4B6';
    setTimeout(function(){ window.location.href = 'login.html'; }, 800);
  });
})();

// Contact form
(function(){
  const contactForm = document.getElementById('contact-form');
  if(!contactForm) return;
  contactForm.addEventListener('submit', function(e){
    e.preventDefault();
    var msg = {
      name: document.getElementById('contact-name').value.trim(),
      phone: document.getElementById('contact-phone').value.trim(),
      email: document.getElementById('contact-email').value.trim(),
      msg: document.getElementById('contact-msg').value.trim(),
      time: new Date().toLocaleString('zh-CN')
    };
    var msgs = JSON.parse(localStorage.getItem('travel_messages') || '[]');
    msgs.push(msg);
    localStorage.setItem('travel_messages', JSON.stringify(msgs));
    document.getElementById('message').textContent = '留言已提交，管理员将在后台查看！';
    document.getElementById('message').style.color = '#2EC4B6';
    contactForm.reset();
  });
})();

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(function(a){
  a.addEventListener('click', function(e){
    var target = document.querySelector(this.getAttribute('href'));
    if(target){ e.preventDefault(); target.scrollIntoView({behavior:'smooth'}); }
  });
});

// Nav active state
(function(){
  var links = document.querySelectorAll('.nav a');
  var page = window.location.pathname.split('/').pop() || 'index.html';
  links.forEach(function(a){
    if(a.getAttribute('href') === page) a.classList.add('active');
  });
})();

// Display current user
(function(){
  var user = JSON.parse(localStorage.getItem('travel_current_user') || 'null');
  var el = document.getElementById('user-status');
  if(el && user){
    el.innerHTML = '<span style="margin-right:10px">欢迎，'+user.name+'</span><a href="#" onclick="localStorage.removeItem(\'travel_current_user\');location.reload()" style="color:var(--gray);font-size:13px">退出</a>';
  }
})();
