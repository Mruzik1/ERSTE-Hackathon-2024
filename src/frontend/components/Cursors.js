import { useEffect } from 'react';
import styles from '@styles/test.module.css';

const CustomCursor = () => {
  useEffect(() => {
    // Очистка консоли для удобства разработки
    // console.clear();

    const circleElement = document.querySelector('.' + styles.circle);

    const mouse = { x: 0, y: 0 };
    const previousMouse = { x: 0, y: 0 };
    const circle = { x: window.innerWidth / 2, y: window.innerHeight / 2 }; // Например, начать из центра экрана
    let currentScale = 0;
    let currentAngle = 0;
    const speed = 0.20;

    const mouseMoveHandler = (e) => {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
    };

    window.addEventListener('mousemove', mouseMoveHandler);

    const tick = () => {
      circle.x += (mouse.x - circle.x) * speed;
      circle.y += (mouse.y - circle.y) * speed;

      const translateTransform = `translate(${circle.x -10 }px, ${circle.y -10 }px)`;

      const deltaMouseX = mouse.x - previousMouse.x;
      const deltaMouseY = mouse.y - previousMouse.y;
      previousMouse.x = mouse.x;
      previousMouse.y = mouse.y;

      const mouseVelocity = Math.min(Math.sqrt(deltaMouseX**2 + deltaMouseY**2) * 4, 150); 

      const stretchStrength = 1.2; 
      const scaleValue = (mouseVelocity / 150) * stretchStrength;
      
      
      currentScale += (scaleValue - currentScale) * speed;
      const scaleTransform = `scale(${1 + currentScale}, ${1 - currentScale})`;

      const angle = Math.atan2(deltaMouseY, deltaMouseX) * 180 / Math.PI;
      if (mouseVelocity > 20) {
        currentAngle = angle;
      }
      const rotateTransform = `rotate(${currentAngle}deg)`;

      circleElement.style.transform = `${translateTransform} ${rotateTransform} ${scaleTransform}`;

      window.requestAnimationFrame(tick);
    };

    tick();

    return () => {
      window.removeEventListener('mousemove', mouseMoveHandler);
    };
  }, []);

  return <div className={styles.circle}></div>;
};

export default CustomCursor;
