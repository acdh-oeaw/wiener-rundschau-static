function toLoris(source) {
  const filename = source.split('/').pop();
  return `https://loris.acdh.oeaw.ac.at/id:wiener-rundschau/${filename}/full/full/0/default.png`;
}

const source = document.getElementById("url").textContent;
var viewer = OpenSeadragon({
  id: "osd_viewer",
  tileSources: {
    type: "image",
    url: toLoris(source),
  },
  prefixUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/openseadragon/4.1.0/images/",
});
