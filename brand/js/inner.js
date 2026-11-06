/* Living Mark inner.js — services and identity pages: before/after slider. */
(function () {
  "use strict";
  const { $ } = window.UV;
  const ba = $("#ba"), range = $("#baRange");
  if (ba && range) {
    const set = () => ba.style.setProperty("--p", range.value + "%");
    range.addEventListener("input", set); set();
  }
})();
