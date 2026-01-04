document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');


  const form = document.getElementById('compose-form');

  form.addEventListener("submit", function (event) {

    event.preventDefault();
    
    const recipients = document.getElementById('compose-recipients').value;
    if (!recipients.trim()) {
      alert("Recipients required");
      return;
    }

    
    const subject = document.getElementById('compose-subject').value;

    const body = document.getElementById('compose-body').value;
    if (!body.trim()) {
      alert("Body required");
      return;
    }

    fetch('/emails', {
      method: 'POST',
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {

        if (result.error) {
          console.error(result.error);
          return;
        }

      load_mailbox('sent');
    
    });
  });
});


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector("#email-view").style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector("#email-view").style.display = 'none';

  // Show the mailbox name
  const emailsView = document.querySelector('#emails-view');
  emailsView.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      const div = document.createElement('div');
      div.className = "email"
      
      let buttonHTML = '';
      if (mailbox === 'inbox') {
        buttonHTML = `<button class="archive-btn btn btn-sm btn-outline-primary" data-id="${email.id}">Archive</button>`;
      }
      else if (mailbox === 'archive') {
        buttonHTML = `<button class="unarchive-btn btn btn-sm btn-outline-primary" data-id="${email.id}">Unarchive</button>`;
      }
      
      let displayName = email.sender;
      if (mailbox === 'sent') {
        displayName = email.recipients.join(', ');
      }

      div.innerHTML = `
      <div class="email-left">
        <strong>${displayName}</strong>
        <span>${email.subject}</span>
        ${buttonHTML}
      </div>
      <span class="email-time">${email.timestamp}</span>
      `;

      if (email.read) {
        div.classList.add("read");
      }

      div.addEventListener('click', () => {
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        })
        .then(() => {
          div.classList.add("read");
          open_email(email.id);
        });
      });

      const archiveButton = div.querySelector(".archive-btn");
      const unarchiveButton = div.querySelector(".unarchive-btn");

      if (archiveButton) {
        archiveButton.addEventListener("click", (event) => {
          event.stopPropagation();
          const id = archiveButton.dataset.id;
          fetch(`/emails/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: true
            })
          })
          .then(() => load_mailbox('inbox'));
        });
      } 
      if (unarchiveButton) {
        unarchiveButton.addEventListener("click", (event) => {
          event.stopPropagation();
          const id = unarchiveButton.dataset.id;
          fetch(`/emails/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: false
            })
          })
          .then(() => load_mailbox('inbox'));
        });
      }
      emailsView.append(div);
    });
  });
}

function open_email(id) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  const emailView = document.querySelector("#email-view");
  emailView.style.display = 'block';

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
   
  emailView.innerHTML = `
  <p><strong>From:</strong> ${email.sender}</p>
  <p><strong>To:</strong> ${email.recipients.join(', ')}</p>
  <p><strong>Subject:</strong> ${email.subject}</p>
  <p><strong>Timestamp:</strong> ${email.timestamp}</p>
  <button id="reply-btn" class="btn btn-sm btn-outline-primary">Reply</button>
  <hr>  
  <p>${email.body}</p>
  `;

  const replyButton = document.getElementById("reply-btn");

  replyButton.addEventListener("click", () => {
    reply_email(email);
  });

  });
}

function reply_email(email) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector("#email-view").style.display = 'none';

  document.querySelector('#compose-recipients').value = email.sender;
  
  if (email.subject && !(email.subject.toLowerCase().startsWith("re:"))) {
    document.querySelector('#compose-subject').value = "Re: " + email.subject;
  }
  else if (email.subject && email.subject.toLowerCase().startsWith("re:")) {
    document.querySelector('#compose-subject').value = email.subject;
  } else {
    document.querySelector('#compose-subject').value = '';
  }

  document.querySelector('#compose-body').value = `\n\nOn ${email.timestamp}, ${email.sender} wrote:\n${email.body}`;
}