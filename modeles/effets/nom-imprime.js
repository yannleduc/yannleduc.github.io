/* Effet « nom imprimé en 3D » (mis de côté, non utilisé sur le site).
   Le titre se dépose couche par couche, de bas en haut, avec une buse qui va et vient,
   et garde des stries de couche comme une vraie pièce FDM.

   Utilisation :
     <div class="printbed"><h1 id="nom">Yann Leduc<span>.</span></h1></div>
     <script src="modeles/effets/nom-imprime.js"></script>
     <script>nomImprime(document.getElementById("nom"), { duree: 2300, couche: 4 });</script>

   CSS minimal :
     .printbed { position: relative; }
     .printbed canvas { position: absolute; left: 0; top: 0; pointer-events: none; }
     .printbed.printing h1, .printbed.printing h1 span { color: transparent; }

   Options : duree (ms), couche (hauteur de couche en px), compteur (élément où écrire « couches : N »).
   Respecte prefers-reduced-motion (affiche directement le résultat). */
function nomImprime(h1, opt) {
  opt = opt || {};
  var bed = h1.parentElement, dur = opt.duree || 2300, LH = opt.couche || 4, cpt = opt.compteur;
  var calm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function go() {
    var old = bed.querySelector("canvas"); if (old) old.remove();
    var r = h1.getBoundingClientRect(), br = bed.getBoundingClientRect();
    var dpr = Math.min(2, window.devicePixelRatio || 1);
    var W = Math.ceil(r.width + 40), H = Math.ceil(r.height + 20);
    var c = document.createElement("canvas");
    c.width = W * dpr; c.height = H * dpr; c.style.width = W + "px"; c.style.height = H + "px";
    c.style.left = (r.left - br.left) + "px"; c.style.top = (r.top - br.top) + "px";
    bed.appendChild(c);
    var x = c.getContext("2d"); x.scale(dpr, dpr);
    var cs = getComputedStyle(h1), sp = h1.querySelector("span"), spanCol = sp ? getComputedStyle(sp).color : cs.color;
    var src = document.createElement("canvas"); src.width = W * dpr; src.height = H * dpr;
    var s = src.getContext("2d"); s.scale(dpr, dpr);
    s.font = cs.fontWeight + " " + cs.fontSize + " " + cs.fontFamily;
    if ("letterSpacing" in s) s.letterSpacing = cs.letterSpacing;
    var base = parseFloat(cs.fontSize) * .78;
    var txt = (h1.firstChild && h1.firstChild.nodeValue || h1.textContent).replace(/\.$/, ""), wTxt = s.measureText(txt).width;
    s.fillStyle = cs.color; s.fillText(txt, 0, base);
    if (sp) { s.fillStyle = spanCol; s.fillText(sp.textContent, wTxt, base); }
    s.globalCompositeOperation = "source-atop"; s.fillStyle = "rgba(255,255,255,.16)";
    for (var y = 0; y < H; y += LH) s.fillRect(0, y, W, 1);
    bed.classList.add("printing");
    var total = Math.ceil(H / LH);
    if (calm) { x.drawImage(src, 0, 0, W, H); if (cpt) cpt.textContent = "couches : " + total; return; }
    var t0 = null;
    function frame(ts) {
      if (!t0) t0 = ts;
      var p = Math.min(1, (ts - t0) / dur), cut = H - H * p;
      x.clearRect(0, 0, W, H);
      x.drawImage(src, 0, cut * dpr, W * dpr, (H - cut) * dpr, 0, cut, W, H - cut);
      if (cpt) cpt.textContent = "couches : " + Math.min(total, Math.floor((H - cut) / LH));
      if (p < 1) {
        var nx = (Math.sin(ts / 90) * .5 + .5) * wTxt;
        x.fillStyle = "#141216"; x.beginPath(); x.moveTo(nx - 9, cut - 16); x.lineTo(nx + 9, cut - 16); x.lineTo(nx + 3, cut - 3); x.lineTo(nx - 3, cut - 3); x.closePath(); x.fill();
        x.fillStyle = "#ffa300"; x.fillRect(nx - 1, cut - 3, 2, 3);
        requestAnimationFrame(frame);
      }
    }
    requestAnimationFrame(frame);
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { setTimeout(go, 200); }); else go();
}
