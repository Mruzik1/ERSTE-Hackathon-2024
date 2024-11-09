import React, { useEffect } from 'react';
import $ from 'jquery';
import { marked } from 'marked';
import '@styles/glass.css';

function scrollToBottom() {
  var messageBody = document.getElementById('messageFormeight');
  messageBody.scrollTop = messageBody.scrollHeight;
}   
   
function Dashboard() {
  useEffect(() => {
    marked.setOptions({
      breaks: true,
      gfm: true,
      sanitize: false,
    });

    // Обработчик отправки формы
    $('#messageArea').on('submit', function (event) {
      event.preventDefault(); // Предотвращаем стандартное поведение формы

      const date = new Date();
      const hour = date.getHours();
      const minute = date.getMinutes();
      const str_time = hour + ':' + minute;

      var rawText = $('#text').val();
      if (!rawText.trim()) {
        return; // Не отправляем пустые сообщения
      }

      // Добавляем сообщение пользователя
      var userHtml =
        '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' +
        rawText +
        '<span class="msg_time_send">' +
        str_time +
        '</span></div><div class="img_cont_msg"><img src="https://i.ibb.co/d5b84Xw/Untitled-design.png" class="rounded-circle user_img_msg"></div></div>';

      $('#text').val(''); // Очищаем поле ввода
      $('#messageFormeight').append(userHtml);
      scrollToBottom();

      // Создаем уникальный идентификатор для ответа бота
      const botResponseId = 'botResponse_' + Date.now();
      var botHtml =
        '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://storage.googleapis.com/gb_chatbot_files_public/Jim%20profil.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer" id="' +
        botResponseId +
        '">' +
        '<span class="msg_time">' +
        str_time +
        '</span></div></div>';

      // Добавляем контейнер для ответа бота
      $('#messageFormeight').append($.parseHTML(botHtml));
      scrollToBottom();

      // Отправляем сообщение пользователя на сервер
      fetch('/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ prompt: rawText }),
      })
        .then((response) => {
          const reader = response.body.getReader();
          const decoder = new TextDecoder();
          let result = '';

          // Функция для чтения потокового ответа
          function read() {
            reader.read().then(({ done, value }) => {
              if (done) {
                console.log('Stream finished');
                return;
              }

              // Декодируем полученные данные
              const chunk = decoder.decode(value, { stream: true });
              console.log('Chunk received:', chunk);
              result += chunk;

              // Парсим Markdown с помощью marked.js
              const markdownContent = marked(result);

              // Обновляем контейнер ответа бота
              $('#' + botResponseId).html(
                markdownContent + '<span class="msg_time">' + str_time + '</span>'
              );

              scrollToBottom();

              // Продолжаем чтение потока
              read();
            });
          }

          // Начинаем чтение потокового ответа
          read();
        })
        .catch((error) => {
          console.error('Error receiving response:', error);
        });
    });
  }, []);

  return (
    <div className='gradient-background w-full h-full'>
      <div className='w-full flex flex-col pt-[30vh] justify-center items-center '>

        <div className='frosted-glass-small gap-7 flex flex-col p-16 px-28  rounded-xl border-2 border-[#FF6D40]'>
          <div className='flex flex-col gap-2 font-extrabold text-7xl text-center text-[#2f2f2f]'>
            <p> <span className='text-[#FF6D40]'>AI</span> Chat </p>
            <p>Assistent</p>
          </div>

          <div className='max-w-6xl p-5 mt-5 border-2  border-[#FF6D40] bg-white rounded-3xl'>
            <form id="messageArea" className='flex gap-x-16'>
              <input type="text" id="text" placeholder="Введите сообщение..." />
              <button type="submit" className='border-1 text-lg text-white uppercase p-3 rounded-3xl bg-[#FF6D40]'>send messages </button>
            </form>
            <div id="messageFormeight">
              {/* Здесь будут отображаться сообщения */}
            </div>
          </div>

        </div>

      </div>
    </div>
  );
}

export default Dashboard;
