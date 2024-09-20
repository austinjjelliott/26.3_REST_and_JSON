// Delete Buttons
$(".delete-cupcake").click(deleteCupcake);

async function deleteCupcake() {
  const id = $(this).data("id");
  await axios.delete(`/api/cupcakes/${id}`); //This deletes it from the db
  $(this).closest(".parent").remove(); //This deletes it from the webpage
}

// Create New Cupcake
$("#cupcake-form").on("submit", async function () {
  // Get form data
  const flavor = $("#flavor").val();
  const size = $('input[name="size"]:checked').val();
  const rating = $("#rating").val();
  const image = $("#imageUrl").val();

  // Send POST request to the API
  await axios.post("/api/cupcakes/", {
    flavor: flavor,
    size: size,
    rating: rating,
    image: image,
  });
});
