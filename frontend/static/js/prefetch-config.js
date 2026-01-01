try {
    const theme = JSON.parse(localStorage.getItem("__SCALO_CONFIG_v3.0__") || "{}").theme;
    if (theme && theme !== "system") document.documentElement.setAttribute("data-theme", theme);
} catch (err) {
    console.log(err);
}
