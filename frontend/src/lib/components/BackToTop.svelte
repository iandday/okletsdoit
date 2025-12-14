<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { writable } from "svelte/store";

    const show = writable(false);

    function toTop() {
        window.scrollTo({ top: 0, behavior: "smooth" });
    }

    let handleScroll: () => void;

    onMount(() => {
        handleScroll = () => show.set(window.pageYOffset > 200);
        window.addEventListener("scroll", handleScroll);
        handleScroll();

        onDestroy(() => {
            window.removeEventListener("scroll", handleScroll);
        });
    });
</script>

<button
    data-show={$show}
    on:click={toTop}
    data-tip="Back to top"
    class="btn tooltip btn-circle translate-y-4 scale-90 opacity-0 transition-all duration-300 data-[show=true]:translate-y-0 data-[show=true]:scale-100 data-[show=true]:opacity-100">
    <span class="iconify lucide--arrow-up size-5.5" />
</button>
