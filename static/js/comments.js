// ----------------------------------------------------------------------------

function addIdtoComment(comment_id) {
  const hiddenInput = document.createElement('input');
  hiddenInput.value = comment_id;
  hiddenInput.hidden = 'true';
  hiddenInput.name = 'comment_id';
  toggleButtonState(false, false);
  
  setTimeout(() => {
    const form = document.getElementById('comment-form');
    form.appendChild(hiddenInput);
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        form.parentElement.replaceChildren();
        toggleButtonState(true, true);
      };
    });
    form.addEventListener('submit', () => {
      toggleButtonState(true, true);
    });
  }, 100);
};
  
function toggleButtonState(isEnabled, isHidden) {
  const buttons = document.querySelectorAll('.replybtn');
  buttons.forEach(button => {
    button.disabled = !isEnabled;
    button.hidden = !isHidden
});
};

const replyAnchors = document.querySelectorAll('.get_replies');
replyAnchors.forEach(replyAnchor => {
  replyAnchor.addEventListener('click', () => {
    const existingHideButton = replyAnchor.parentNode.querySelectorAll('.hide');
    if (existingHideButton.length < 1) {
      const hideButton = document.createElement('button');
      hideButton.textContent = 'Hide';
      hideButton.classList.add('hide', 'card-link', 'text-primary');
      hideButton.style.border = 'none';
      hideButton.style.outline = 'none';
      hideButton.style.backgroundColor = 'white';
      replyAnchor.parentNode.insertBefore(hideButton, replyAnchor.nextSibling);

      hideButton.addEventListener('click', () => {
        const target = document.querySelector('.replies_body');
        setTimeout(() => {
          target.parentNode.replaceChildren();
          hideButton.remove();
        }, 100);
      });
    } 
  });
});
