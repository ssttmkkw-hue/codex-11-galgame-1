"use strict";
(() => {
  const assets = window.ART_CATALOG?.assets || [];
  const expressions = {neutral:"日常",smile:"喜悦",shy:"害羞",surprised:"惊讶",serious:"认真",sad:"落泪"};
  const names = {natsumi:"夏澄",mio:"澪"};
  const stage = document.getElementById("stage");
  const scene = document.getElementById("scene");
  const status = document.getElementById("status");
  const state = {background:"seawall_day",natsumi:"neutral",mio:"neutral"};
  const backgrounds = assets.filter(asset => asset.category === "background");
  const selector = document.getElementById("background");
  const src = asset => `../${asset.path}`;

  function describe() {
    const location = backgrounds.find(asset => asset.id === state.background)?.label || "场景";
    const characters = Object.keys(names).filter(id => !document.getElementById(id).hidden)
      .map(id => `${names[id]}（${expressions[state[id]]}）`).join("、");
    stage.setAttribute("aria-label",`${location}，${characters || "无角色"}`);
    status.textContent = stage.getAttribute("aria-label");
  }

  for (const asset of backgrounds) {
    const option = document.createElement("option");
    option.value = asset.id;
    option.textContent = asset.label;
    selector.append(option);
  }
  selector.value = state.background;
  selector.addEventListener("change", () => {
    const asset = backgrounds.find(asset => asset.id === selector.value);
    if (!asset) return;
    state.background = asset.id;
    scene.src = src(asset);
    scene.alt = asset.label;
    document.getElementById("scene-tag").textContent = `汐见 · ${asset.label}`;
    describe();
  });

  for (const id of Object.keys(names)) {
    const group = document.getElementById(`${id}-expressions`);
    group.setAttribute("role","group");
    group.setAttribute("aria-label",`${names[id]}的表情`);
    for (const [expression,label] of Object.entries(expressions)) {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = label;
      button.dataset.expression = expression;
      button.setAttribute("aria-pressed",String(expression === "neutral"));
      button.addEventListener("click", () => {
        const image = document.getElementById(id);
        state[id] = expression;
        image.src = `../assets/characters/${id}/${expression}.png`;
        image.alt = `${names[id]}，${label}表情`;
        for (const sibling of group.children) sibling.setAttribute("aria-pressed",String(sibling === button));
        describe();
      });
      group.append(button);
    }
    document.getElementById(`show-${id}`).addEventListener("change", event => {
      document.getElementById(id).hidden = !event.target.checked;
      describe();
    });
  }

  document.getElementById("fullbody").addEventListener("change",event => stage.classList.toggle("fullbody",event.target.checked));
  document.getElementById("checker").addEventListener("change",event => stage.classList.toggle("checker",event.target.checked));
  document.getElementById("show-dialogue").addEventListener("change",event => document.getElementById("dialogue").hidden = !event.target.checked);

  const grid = document.getElementById("asset-grid");
  for (const asset of assets) {
    const card = document.createElement("a");
    card.className = `asset-card ${asset.category}`;
    card.dataset.category = asset.category;
    card.href = src(asset);
    card.target = "_blank";
    card.rel = "noopener";
    const thumb = document.createElement("div");
    thumb.className = "thumb";
    const image = document.createElement("img");
    image.src = src(asset);
    image.alt = asset.label;
    image.loading = "lazy";
    image.decoding = "async";
    thumb.append(image);
    const title = document.createElement("h3");
    title.textContent = asset.label;
    const arrow = document.createElement("span");
    arrow.textContent = "↗";
    arrow.setAttribute("aria-hidden","true");
    title.append(arrow);
    const detail = document.createElement("p");
    detail.textContent = `${asset.width} × ${asset.height} · PNG${asset.has_alpha ? " / ALPHA" : ""} · ${(asset.bytes/1024/1024).toFixed(1)} MB`;
    card.append(thumb,title,detail);
    grid.append(card);
  }
  for (const button of document.querySelectorAll("[data-filter]")) {
    button.addEventListener("click", () => {
      const filter = button.dataset.filter;
      for (const sibling of document.querySelectorAll("[data-filter]")) sibling.setAttribute("aria-pressed",String(sibling === button));
      let count = 0;
      for (const card of grid.children) {
        card.hidden = filter !== "all" && card.dataset.category !== filter;
        if (!card.hidden) count++;
      }
      document.getElementById("asset-count").textContent = `${count} 张原始 PNG${filter === "all" ? " / 5 类素材" : ""}`;
      status.textContent = `已显示 ${count} 张${button.textContent}素材`;
    });
  }
  describe();
})();
