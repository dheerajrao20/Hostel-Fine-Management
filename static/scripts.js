$(document).ready(function() {
    $("#add-fine-form").submit(function(e) {
        e.preventDefault();

        const room = $("#room").val();
        const fine_to_add = $("#fine_to_add").val();

        $.post("/add_fine", { room, fine_to_add }, function(response) {
            alert(response.message);
        });

        $("#room").val(""); // Clear the room field
        $("#fine_to_add").val(""); // Clear the name field
    });

    $("#remove-fine-form").submit(function(e) {
        e.preventDefault();

        const room = $("#room").val();
        const fine_to_remove = $("#fine_to_remove").val();

        $.post("/remove_fine", { room, fine_to_remove }, function(response) {
            alert(response.message);
        });

        $("#room").val(""); // Clear the room field
        $("#fine_to_remove").val(""); // Clear the name field
    });

    $("#insert-student-form").submit(function(e) {
        e.preventDefault();

        const name = $("#name").val();
        const room = $("#room").val();

        $.post("/insert_student", { name, room }, function(response) {
            alert(response.message);  // Display an alert with the success message
        });

        $("#name").val(""); // Clear the name field
        $("#room").val(""); // Clear the room field
    });
});
