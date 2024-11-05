function adjustTitleFontSize() {
    const titleElements = document.querySelectorAll('.item-name');

    titleElements.forEach(titleElement => {
        const maxFontSize = 13;
        const minFontSize = 11;
        const maxTitleLength = 50;

        let titleLength = titleElement.textContent.length;

        let newTitleSize = maxFontSize - (titleLength - maxTitleLength);

        newTitleSize = Math.max(minFontSize, Math.min(maxFontSize, newTitleSize));
        titleElement.style.fontSize = `${newTitleSize}px`;
    });
}

window.onload = adjustTitleFontSize;
