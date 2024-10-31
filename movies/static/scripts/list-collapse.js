var collapse_item = document.getElementsByClassName('collapsible')

var i;

for (i = 0; i < collapse_item.length; i++){
    collapse_item[i].addEventListener('click', function () {
        this.classList.toggle("active");
        var content = this.nextElementSibling;

        if (content.style.display === 'flex'){
            content.style.display = 'none';    
        }
        else{
            content.style.display = 'flex';
        }

    });
}