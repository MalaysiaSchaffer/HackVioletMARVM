// Initialize Supabase

// import { createClient } from "@supabase/supabase-js";
const supabaseUrl = "https://gbitdizurwmvqogihplg.supabase.co";
const supabaseKey =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdiaXRkaXp1cndtdnFvZ2locGxnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzg0MzYyODgsImV4cCI6MjA1NDAxMjI4OH0.bJCOwwDSQZqGHzMFq7PiPkaiYcqfzcKDA5fCNQIo3G0"; // Keep this secure
const supabased = supabase.createClient(
  "https://gbitdizurwmvqogihplg.supabase.co",
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdiaXRkaXp1cndtdnFvZ2locGxnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzg0MzYyODgsImV4cCI6MjA1NDAxMjI4OH0.bJCOwwDSQZqGHzMFq7PiPkaiYcqfzcKDA5fCNQIo3G0"
);

// ✅ Initialize Supabase (No Import Needed)
// const supabase = window.supabase.createClient(
//   "https://gbitdizurwmvqogihplg.supabase.co",
//   "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdiaXRkaXp1cndtdnFvZ2locGxnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzg0MzYyODgsImV4cCI6MjA1NDAxMjI4OH0.bJCOwwDSQZqGHzMFq7PiPkaiYcqfzcKDA5fCNQIo3G0"
// );

const bucketName = "First"; // Your Supabase storage bucket
const totalImages = 7;
let currentIndex = 1;
const userId = "user_123"; // Replace this with Supabase Auth later

// ✅ Function to update image source
async function updateImage() {
  const imageUrl = `${supabaseUrl}/storage/v1/object/public/${bucketName}/${currentIndex}.png`;
  document.getElementById("image-display").src = imageUrl;

  // Fetch existing user input for this image
  await loadUserInput();
}

// ✅ Fetch user input for the current image
async function loadUserInput() {
  const imageName = `${currentIndex}.png`;

  const { data, error } = await supabased
    .from("user_inputs")
    .select("input_text")
    .eq("user_id", userId)
    .eq("image_name", imageName)
    .order("created_at", { ascending: false }) // Get latest input
    .limit(1)
    .single();

  if (error) {
    console.warn("No previous input found or access issue.", error);
    document.getElementById("user-input").value = "";
  } else if (data) {
    console.log("Loaded input:", data);
    document.getElementById("user-input").value = data.input_text;
  }
}

// ✅ Save user input (Always creates a new row)
async function saveUserInput() {
  const imageName = `${currentIndex}.png`;
  const inputText = document.getElementById("user-input").value;

  const { data, error } = await supabased
    .from("user_inputs")
    .insert([
      { user_id: userId, image_name: imageName, input_text: inputText },
    ]);
  console.log(data);
  if (error) {
    console.error("Error saving input:", error);
  } else {
    console.log("Saved:", data);
    document.getElementById("saved-message").style.display = "block";
    setTimeout(
      () => (document.getElementById("saved-message").style.display = "none"),
      2000
    );
  }
}

// ✅ Handle Next button click
document.getElementById("next-btn").addEventListener("click", () => {
  currentIndex = (currentIndex % totalImages) + 1;
  updateImage();
});

// ✅ Handle Save button click
document.getElementById("save-btn").addEventListener("click", saveUserInput);

// ✅ Load first image on page load
updateImage();
