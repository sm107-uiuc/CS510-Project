const port = chrome.runtime.connect({ name: "popup" });

const renderUrlList = (urls) => {
  const urlListContainer = document.getElementById("url-list");

  urls.forEach((url) => {
    const listItem = document.createElement("li");
    const link = document.createElement("a");

    link.href = url;
    link.textContent = url;
    link.target = "_blank";

    listItem.appendChild(link);
    urlListContainer.appendChild(listItem);
  });
};

port.onMessage.addListener((message) => {
  if (message.urls) {
    renderUrlList(message.urls);
  }
});

port.postMessage({ action: "getUrls" });

// Disconnect the port when the window is closed
window.addEventListener("unload", () => {
  port.disconnect();
});
