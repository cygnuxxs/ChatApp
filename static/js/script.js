
const themeMap = {
    dark: "light",
    light: "solar",
    solar: "dark"
};

const theme = localStorage.getItem('theme')
    || (tmp = Object.keys(themeMap)[0],
        localStorage.setItem('theme', tmp),
        tmp);
const bodyClass = document.body.classList;
bodyClass.add(theme);

function toggleTheme() {
    const current = localStorage.getItem('theme');
    const next = themeMap[current];

    bodyClass.replace(current, next);
    localStorage.setItem('theme', next);
}

document.getElementById('themeButton').onclick = toggleTheme;

const Contents = document.getElementsByClassName("tabContent");
for (const content of Contents) {
    content.style.display = "none";
}

function openTab(anchor, tabName) {
    const tabContents = document.getElementsByClassName('tabContent');
    for (const tab of tabContents) {
        tab.style.display = "none";
    }
    const selectedTab = document.getElementById(tabName);
    selectedTab.style.display = "flex";
    const navLinks = document.getElementsByClassName('navLink');
    for (const link of navLinks) {
        link.classList.remove("active");
    }
    anchor.classList.add("active");
    event.preventDefault();
}

function openMsg(anchor, msgTab) {
    anchor.classList.add('active');
}