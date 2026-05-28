function gameApp() {
    return {
        query: '',
        searchResults: [],
        showResults: false,
        selectedGames: [],
        recommendations: [],
        loading: false,
        hasSearched: false,

        activeIndex: -1,

        formatGenres(genres) {
            if (!genres) return '';
            try {
                const parsed = JSON.parse(genres.replace(/'/g, '"'));
                if (Array.isArray(parsed)) return parsed.join(', ');
            } catch (e) {}
            return genres.replace(/[\[\]']/g, '').trim();
        },

        truncate(text, max) {
            if (!text) return '';
            return text.length > max ? text.slice(0, max) + '…' : text;
        },

        igdbUrl(game) {
            if (!game || !game.slug) return `https://www.igdb.com/search?q=${encodeURIComponent(game?.name || '')}`;
            return `https://www.igdb.com/games/${game.slug}`;
        },

        async search() {
            if (this.query.length < 2) {
                this.searchResults = [];
                this.showResults = false;
                this.activeIndex = -1;
                return;
            }
            const res = await fetch(`/search?q=${encodeURIComponent(this.query)}&limit=8`);
            this.searchResults = await res.json();
            this.showResults = true;
            this.activeIndex = -1;
        },

        handleKeydown(e) {
            if (!this.showResults || this.searchResults.length === 0) return;

            if (e.key === 'ArrowDown') {
                e.preventDefault();
                this.activeIndex = (this.activeIndex + 1) % this.searchResults.length;
                this.scrollToActive();
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                this.activeIndex = this.activeIndex <= 0 ? this.searchResults.length - 1 : this.activeIndex - 1;
                this.scrollToActive();
            } else if (e.key === 'Enter') {
                e.preventDefault();
                if (this.activeIndex >= 0) {
                    this.selectGame(this.searchResults[this.activeIndex]);
                }
            } else if (e.key === 'Escape') {
                this.showResults = false;
                this.activeIndex = -1;
            }
        },

        scrollToActive() {
            setTimeout(() => {
                const container = document.querySelector('.search-results');
                if (!container) return;
                const items = container.querySelectorAll('.search-item');
                const active = items[this.activeIndex];
                if (active) {
                    active.scrollIntoView({ block: 'nearest', inline: 'nearest' });
                }
            }, 10);
        },

        selectGame(game) {
            if (!this.selectedGames.find(g => g.id === game.id)) {
                this.selectedGames.push(game);
            }
            this.query = '';
            this.searchResults = [];
            this.showResults = false;
        },

        removeGame(id) {
            this.selectedGames = this.selectedGames.filter(g => g.id !== id);
        },

        async getRecommendations() {
            this.loading = true;
            this.hasSearched = true;
            const ids = this.selectedGames.map(g => g.id);
            const res = await fetch('/get-recommendations', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ game_ids: ids })
            });
            this.recommendations = await res.json();
            this.loading = false;
        }
    };
}
