<script>
document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.messages li');
    messages.forEach((message) => {
        setTimeout(() => {
            message.classList.add('hide');
        }, 5000);
    });
});
</script>