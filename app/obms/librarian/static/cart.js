document.addEventListener('DOMContentLoaded', function() {
    const cartList = document.getElementById('cartList');
    const cartForm = document.getElementById('cart-form');

    var myInput;

    // Display books in the list
    i = 0;
    books.forEach(book => {
        const listItem = document.createElement('div');
        listItem.classList.add('cart-list-item');
        listItem.textContent = book.title;

        const label = document.createElement('label');
        label.style.float = 'right';
        label.style.transform = 'translateY(-6px)';
        label.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16"><path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/><path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/></svg>'
        label.classList.add("btn");
        label.classList.add("btn-secondary");
        label.style.float = 'right';
        const input = document.createElement('input');
        input.id = `return`
        input.type = 'submit';
        input.style.display = 'none';
        input.style.visibility = 'hidden';
        myInput = input;


        label.htmlFor = input.id;
        listItem.appendChild(label);

        listItem.addEventListener('click', () => {
            displayCartDetails(book);
        });
        cartList.appendChild(listItem);
        i++;
    });



    // Function to display book details
    function displayCartDetails(book) {
        $("#cart-form").html("");

        const csrf = document.createElement('input');
        csrf.type = 'hidden';
        csrf.name = 'csrfmiddlewaretoken';
        csrf.value = document.querySelector('[name=csrfmiddlewaretoken]').value;
        cartForm.append(csrf);

        const id = document.createElement('label');
        id.classList.add('td');
        id.htmlFor = "id_id";
        id.style.display = 'none';
        id.style.visibility = 'hidden';
        id.innerHTML = `<input id="id_id" type="hidden" name="id" value=${book.id}></input>`

        const title = document.createElement('label');
        title.classList.add('td');
        title.htmlFor = "id_title";
        title.innerHTML = `${book.title}<input id="id_title" type="hidden" name="title" value=${book.title}></input>`

        const author = document.createElement('label');
        author.classList.add('td');
        author.htmlFor = "id_author";
        author.innerHTML = `${book.author}<input id="id_author" type="hidden" name="author" value=${book.author}></input>`

        const genre = document.createElement('label');
        genre.classList.add('td');
        genre.htmlFor = "id_genre";
        genre.innerHTML = `${book.genre}<input id="id_genre" type="hidden" name="genre" value=${book.genre}></input>`

        const checkedOut = document.createElement('label');
        checkedOut.classList.add('td');
        checkedOut.htmlFor = "id_checkedOut";
        checkedOut.innerHTML = `${!book.checkedOut}<input id="id_checkedOut" type="hidden" name="checkedOut" value=${book.checkedOut}></input>`

        cartForm.appendChild(id);
        cartForm.appendChild(title);
        cartForm.appendChild(author);
        cartForm.appendChild(genre);
        cartForm.appendChild(checkedOut);
        cartForm.appendChild(myInput);
    }

    // const bookList = document.getElementById('bookList');
    // const bookDetails = document.getElementById('bookDetails');

    // // Display books in the list
    // libraryBooks.forEach(book => {
    //     const listItem = document.createElement('div');
    //     listItem.classList.add('cart-list-item');
    //     listItem.textContent = book.title;
    //     listItem.addEventListener('click', () => {
    //         displayBookDetails(book);
    //     });
    //     bookList.appendChild(listItem);
    // });

    // // Function to display book details
    // function displayBookDetails(book) {
    //     bookDetails.innerHTML = `
    //         <h2>${book.title}</h2>
    //         <p>By: ${book.author}</p>
    //     `;
    // }


});

