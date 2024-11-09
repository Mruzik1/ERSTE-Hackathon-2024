import React, { useEffect } from 'react';
import $ from 'jquery';
import '@styles/dashboard.css';

function scrollToBottom() {
  var messageBody = document.getElementById('messageFormeight');
  messageBody.scrollTop = messageBody.scrollHeight;
}   

function Dashboard() {
  useEffect(() => {
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
      fetch('http://localhost:5000/chat', {
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

              $("#" + botResponseId).html(result + '<span class="msg_time">' + str_time + '</span>');

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
    <><>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/dompurify@2.2.9/dist/purify.min.js"></script>
    <link
      rel="stylesheet"
      href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"
      integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO"
      crossorigin="anonymous" /><link
        rel="stylesheet"
        href="https://use.fontawesome.com/releases/v5.5.0/css/all.css"
        integrity="sha384-B4dIYHKNBt8Bc12p+WXckhzcICo0wtJAoU8YZTY5qE0Id1GSseTk6S+L3BlXeVIU"
        crossorigin="anonymous" /><script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
        </>
        <div className='gradient-background w-full h-full'>
          <div class="row justify-content-center h-100">
            <div class="col-md-11 col-xl-6 chat">
              <div class="card">
                <div class="card-header msg_head">
                  <p> <span className='text-[#FF6D40]'>AI</span> Assistant </p>
                </div>

                <div id="messageFormeight" class="card-body msg_card_body">
                  {/* Здесь будут отображаться сообщения */}
                </div>
                <div class="card-footer">
                  <form id="messageArea" class="input-group">
                    <input type="text" id="text" name="msg" class="form-control type_msg" placeholder="Введите сообщение..." autoComplete='off' required />
                    <div class="input-group-append">
                      <button type="submit" id="send" class="input-group-text send_btn">
                        <i class="fas fa-location-arrow"></i>
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </>
  );
}

export default Dashboard;
