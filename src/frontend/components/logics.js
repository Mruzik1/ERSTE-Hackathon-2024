import React, { useEffect } from 'react';
import $ from 'jquery';
import { marked } from 'marked';

function scrollToBottom() {
  var messageBody = document.getElementById('messageFormeight');
  messageBody.scrollTop = messageBody.scrollHeight;
}

function ChatComponent() {
  useEffect(() => {
    $(document).ready(function () {
      marked.setOptions({
        breaks: true,
        gfm: true,
        sanitize: false,
      });

      $('#messageArea').on('submit', function (event) {
        event.preventDefault();

        const date = new Date();
        const hour = date.getHours();
        const minute = date.getMinutes();
        const str_time = hour + ':' + minute;

        var rawText = $('#text').val();
        if (!rawText.trim()) {
          return;
        }

        var userHtml =
          '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' +
          rawText +
          '<span class="msg_time_send">' +
          str_time +
          '</span></div><div class="img_cont_msg"><img src="https://i.ibb.co/d5b84Xw/Untitled-design.png" class="rounded-circle user_img_msg"></div></div>';

        $('#text').val('');
        $('#messageFormeight').append(userHtml);
        scrollToBottom();

        const botResponseId = 'botResponse_' + Date.now();
        var botHtml =
          '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://storage.googleapis.com/gb_chatbot_files_public/Jim%20profil.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer" id="' +
          botResponseId +
          '">' +
          '<span class="msg_time">' +
          str_time +
          '</span></div></div>';

        $('#messageFormeight').append($.parseHTML(botHtml));
        scrollToBottom();

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

            function read() {
              reader.read().then(({ done, value }) => {
                if (done) {
                  console.log('Stream finished');
                  return;
                }

                const chunk = decoder.decode(value, { stream: true });
                console.log('Chunk received:', chunk);
                result += chunk;

                const markdownContent = marked(result);

                $('#' + botResponseId).html(
                  markdownContent + '<span class="msg_time">' + str_time + '</span>'
                );

                scrollToBottom();

                read();
              });
            }

            read();
          })
          .catch((error) => {
            console.error('Error receiving response:', error);
          });
      });
    });
  }, []);

  return (
    <div>
      <form id="messageArea">
        <input type="text" id="text" />
        <button type="submit">Отправить</button>
      </form>
      <div id="messageFormeight">
        {/* Сообщения будут добавляться здесь */}
      </div>
    </div>
  );
}

export default ChatComponent;
