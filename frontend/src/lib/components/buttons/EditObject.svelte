<script lang="ts">
    type iEditObjectProps = {
        href: string;
        label: string;
    };

    const { href, label }: iEditObjectProps = $props();
</script>

<button class="btn btn-success btn-sm gap-2" onclick={() => (window.location.href = href)}>
    <span class="icon-[lucide--edit] size-5"></span>
    {label}
</button>
