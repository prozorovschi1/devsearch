
  // Obține formularul de căutare și link-urile paginilor
  let searchForm = document.getElementById("searchForm");
  let pageLinks = document.getElementsByClassName("page-link");

  // Asigură-te că formularul de căutare există
  if (searchForm) {
    for (let i = 0; i < pageLinks.length; i++) {
      pageLinks[i].addEventListener("click", function (e) {
        e.preventDefault(); // Evită comportamentul implicit al linkului
        // Obține atributul data-page
        let page = this.dataset.page;

        // Adaugă un input ascuns în formular
        searchForm.innerHTML += `<input value="${page}" name="page" hidden />`;

        // Trimite formularul
        searchForm.submit();
      });
    }
  }
