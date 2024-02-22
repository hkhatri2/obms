setInterval(function(){ $(".alert").fadeOut(); }, 3000);

const searchInput = document.getElementById('searchInput');
const resultsList = document.getElementById('results');

let sorter = '';
$(function(){
    $('#browse').trigger('click');
 });

$('button').on('click', function(){
    $('button').removeClass('selected');
    $(this).addClass('selected');
    sorter = $(this).val();
    if (!sorter) {
        displayResults(objects);
    } else {
        displayResults([]);
    }
    $("#searchInput").val('');

});

searchInput.addEventListener('input', (event) => {
    const query = event.target.value.toLowerCase();
    var filteredObjects = objects;
    if (sorter) {
        filteredObjects = objects.filter(object =>
            object[sorter].toLowerCase().includes(query)
        );
    }
    if (query) {
        displayResults(filteredObjects);
    } else {
        displayResults([]);
    }

});

function displayResults(results) {
    resultsList.innerHTML = '';
    if (results.length === 0) {
        table = document.getElementById('book-list');
        resultsList.innerHTML = '<div class="tr"><div class="td"></div><div class="td"></div><div class="td">No results found. </br> Edit search query.</div><div class="td"></div><div class="td"></div></div>';
        table.appendChild(resultsList);
    } else {
        i = 0;
        results.forEach(result => {

            const csrf = document.createElement('input');
            csrf.type = 'hidden';
            csrf.name = 'csrfmiddlewaretoken';
            csrf.value = document.querySelector('[name=csrfmiddlewaretoken]').value;

            const form = document.createElement('form');
            form.method = "POST";
            form.append(csrf);
            form.classList.add('tr');

            const id = document.createElement('label');
            id.classList.add('td');
            id.htmlFor = "id_id";
            id.style.display = 'none';
            id.style.visibility = 'hidden';
            id.innerHTML = `<input id="id_id" type="hidden" name="id" value=${result.id}></input>`

            const title = document.createElement('label');
            title.classList.add('td');
            title.htmlFor = "id_title";
            title.innerHTML = `${result.title}<input id="id_title" type="hidden" name="title" value=${result.title}></input>`

            const author = document.createElement('label');
            author.classList.add('td');
            author.htmlFor = "id_author";
            author.innerHTML = `${result.author}<input id="id_author" type="hidden" name="author" value=${result.author}></input>`

            const genre = document.createElement('label');
            genre.classList.add('td');
            genre.htmlFor = "id_genre";
            genre.innerHTML = `${result.genre}<input id="id_genre" type="hidden" name="genre" value=${result.genre}></input>`

            const checkedOut = document.createElement('label');
            checkedOut.classList.add('td');
            checkedOut.htmlFor = "id_checkedOut";
            checkedOut.innerHTML = `${!result.checkedOut}<input id="id_checkedOut" type="hidden" name="checkedOut" value=${result.checkedOut}></input>`

            const label = document.createElement('label');
            label.classList.add('td');
            label.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cart" viewBox="0 0 16 16"><path d="M0 1.5A.5.5 0 0 1 .5 1H2a.5.5 0 0 1 .485.379L2.89 3H14.5a.5.5 0 0 1 .491.592l-1.5 8A.5.5 0 0 1 13 12H4a.5.5 0 0 1-.491-.408L2.01 3.607 1.61 2H.5a.5.5 0 0 1-.5-.5M3.102 4l1.313 7h8.17l1.313-7zM5 12a2 2 0 1 0 0 4 2 2 0 0 0 0-4m7 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4m-7 1a1 1 0 1 1 0 2 1 1 0 0 1 0-2m7 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2"/></svg>'
            label.classList.add("btn");
            label.classList.add("btn-secondary");
            label.classList.add("checkout");
            const input = document.createElement('input');
            input.classList.add("checkout");
            input.type = 'submit';
            input.style.display = 'none';
            input.style.visibility = 'hidden';
            label.appendChild(input);

            form.append(id, title, author, genre, checkedOut, label);
            resultsList.appendChild(form);
            table = document.getElementById('book-list');
            table.appendChild(resultsList);
            i++;
        });
    }
}

