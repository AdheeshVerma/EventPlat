function toggleDisplay() {
    const element = document.getElementById('menu_lst');
    
    if (element.style.display === "none") {
        element.style.display = "flex";
    } else {
        element.style.display = "none";
    }
}