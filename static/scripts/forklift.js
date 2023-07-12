const tableHeader1 = document.getElementById("table_header_1");
const tableHeader2 = document.getElementById("table_header_2");
const tableHeader3 = document.getElementById("table_header_3");

function updateTable(url, header1, header2, header3) {
    fetch(url)
      .then(response => response.text())
      .then(html => {
        const tableHtml = new DOMParser().parseFromString(html, 'text/html').querySelector('#table-container').innerHTML;
        document.querySelector('#table-container').innerHTML = tableHtml;

        const tableHeader1 = document.getElementById("table_header_1");
        const tableHeader2 = document.getElementById("table_header_2");
        const tableHeader3 = document.getElementById("table_header_3");

        tableHeader1.style.display = header1;
        tableHeader2.style.display = header2;
        tableHeader3.style.display = header3;
      });
  }

  document.querySelector('#table1-button').addEventListener('click', () => {
    updateTable(`/forklifts/${document.querySelector('#table1-button').getAttribute('data-id')}/`, 'block', 'none', 'none');
  });
  
  document.querySelector('#table2-button').addEventListener('click', () => {
    updateTable('/tos/', 'none', 'block', 'none');
  });
  
  document.querySelector('#table3-button').addEventListener('click', () => {
    updateTable('/claims/', 'none', 'none', 'block');
  });