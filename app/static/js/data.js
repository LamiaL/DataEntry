function setupDataTable({
    tableId,
    basePath = "",   
    limit = 20
}) {
    let dataTable = null;

    const fetchUrl = `${basePath ? "/" + basePath : ""}/get_data_${tableId}`;
    const editPath = `${basePath ? "/" + basePath : ""}/edit_${tableId}`;
    const deletePath = `${basePath ? "/" + basePath : ""}/delete_data_${tableId}`;
   
    function fetchData() {
        let url = fetchUrl;
       

        fetch(url)
            .then(response => response.json())
            .then(data => {
                const tbody = document.querySelector(`#${tableId} tbody`);
                tbody.innerHTML = "";

                if (data.length === 0) return;

                const columnOrder = Array.from(document.querySelectorAll(`#${tableId} thead tr:first-child th[data-column]`))
                         .map(th => th.getAttribute("data-column"));

                data.forEach(row => {
                    const tr = document.createElement("tr");
                    let rowHtml = `
                        <td>
                            <select class="action-select">
                                <option value="" disabled selected> </option>
                                <option value="edit">Modifier</option>
                                <option value="delete">Supprimer</option>
                            </select>
                        </td>`;

                    columnOrder.forEach(col => {
                        rowHtml += `<td>${row[col]}</td>`;
                    });

                    tr.innerHTML = rowHtml;
                    tbody.appendChild(tr);
                });

                if (dataTable) {
                    dataTable.destroy();
                }
                
                dataTable = $(`#${tableId}`).DataTable({
                    orderCellsTop: true,
                    fixedHeader: false,
                    info: false,
                    lengthMenu: [[20, 50, 100, 200, -1], [20, 50, 100, 200, "Tous"]],
                    pageLength: parseInt(limit) || 20,
                    language: {
                        lengthMenu: "Afficher _MENU_ lignes par page",
                        zeroRecords: "Aucun résultat trouvé",
                        info: "Page _PAGE_ sur _PAGES_",
                        infoEmpty: "Aucune donnée disponible",
                        infoFiltered: "(filtré de _MAX_ total lignes)",
                        search: "Rechercher:"
                    }
                });

                $(`#${tableId} thead tr:eq(1) th`).each(function (i) {
                    const input = $(this).find('input, select');
                    input.off().on('change keyup', function () {
                        const val = this.value;
                        if (dataTable.column(i).search() !== val) {
                            dataTable.column(i).search(val).draw();
                        }
                    });
                });

                document.querySelectorAll(".action-select").forEach(select => {
                    select.addEventListener("change", function () {
                        const action = this.value;
                        const row = this.closest("tr");
                        const rowId = row.querySelector("td:nth-child(2)").textContent;

                        if (action === "edit") {
                            window.location.href = `${editPath}/${rowId}`;
                        } else if (action === "delete") {
                            const confirmation = confirm("Vous voulez supprimer cette ligne?");
                            if (confirmation) {
                                deleteRow(rowId, row);
                            } else {
                                this.selectedIndex = 0;
                            }
                        }
                    });
                });
            })
            .catch(error => console.error("Error fetching data:", error));
    }

    function deleteRow(id, row) {
        fetch(`${deletePath}/${id}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                row.remove();
                alert("Row deleted successfully");
            } else {
                alert("Error deleting row");
            }
        })
        .catch(error => {
            console.error("Error deleting row:", error);
            alert("Error deleting row");
        });
    }

    fetchData();
}
// get users list then difine a filtering logic by exact user name
fetch('/get_usernames')
  .then(res => res.json())
  .then(usernames => {
    const select = document.getElementById("filter-agent");
    usernames.forEach(username => {
      const option = document.createElement("option");
      option.value = username;
      option.textContent = username;
      select.appendChild(option);
    });
   $.fn.dataTable.ext.search.push(
      function(settings, data, dataIndex) {
       const selected = $('#filter-agent').val();
       const username = data[2].trim(); // column index 2
      return selected === "" || username === selected;
   });
   $('#filter-agent').on('change', function () {
    dataTable.draw();
     });
});
