function codexLoading(loadingId, resultId) {
  const loading = document.getElementById(loadingId);
  if (loading) loading.classList.remove("hidden");

  // Hide previous result while loading (better UX)
  const result = document.getElementById(resultId);
  if (result) result.style.display = "none";

  // allow form submit
  return true;
}
