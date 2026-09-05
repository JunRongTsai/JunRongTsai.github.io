// 所有遊戲共用的開始 / 結束 / 暫停畫面控制。
// 每款遊戲只要在 body 內放一份 .game-overlay 標準結構 (見任一遊戲頁)，
// 就能透過 GameUI.show() 取得一致的標題卡、開始按鈕與操作說明。
(function () {
    let root, titleEl, subEl, statsEl, btnEl, controlsEl;

    function ensure() {
        if (root) return true;
        root = document.getElementById('game-overlay');
        if (!root) return false;
        titleEl = document.getElementById('overlay-title');
        subEl = document.getElementById('overlay-sub');
        statsEl = document.getElementById('overlay-stats');
        btnEl = document.getElementById('overlay-btn');
        controlsEl = document.getElementById('overlay-controls');
        return true;
    }

    window.GameUI = {
        // onButton 一律用 onclick 指派：每次 show() 都會覆蓋上一個處理器，
        // 避免「開始 / 重來 / 繼續」三種狀態的監聽器疊加後被一次全部觸發
        show: function (opts) {
            if (!ensure()) return;
            opts = opts || {};
            titleEl.textContent = opts.title || '';
            subEl.textContent = opts.sub || '';
            statsEl.textContent = opts.stats || '';
            btnEl.textContent = opts.button || '開始遊戲';
            btnEl.onclick = opts.onButton || null;
            if (controlsEl) controlsEl.classList.toggle('hidden', !opts.controls);
            root.classList.remove('hidden');
        },
        hide: function () {
            if (ensure()) root.classList.add('hidden');
        },
        get isVisible() {
            return ensure() ? !root.classList.contains('hidden') : false;
        }
    };

    // 覆蓋層顯示時，Space / Enter 等同按下主要按鈕，五款遊戲的起始操作因此一致。
    // 這個監聽器比各遊戲的早註冊 (game-ui.js 先載入)，所以用 stopImmediatePropagation
    // 擋掉同一個事件繼續傳給遊戲本身 —— 否則按下 Space 開始遊戲後，
    // 遊戲的按鍵處理會把同一次按鍵當成操作 (貪食蛇會立刻暫停、俄羅斯方塊會立刻硬降)。
    document.addEventListener('keydown', function (e) {
        if (!ensure() || root.classList.contains('hidden')) return;
        if (e.key === ' ' || e.key === 'Spacebar' || e.key === 'Enter') {
            e.preventDefault();
            e.stopImmediatePropagation();
            if (btnEl.onclick) btnEl.click();
        }
    });
})();
