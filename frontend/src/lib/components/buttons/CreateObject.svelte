<script lang="ts">
    type iCreateObjectProps = {
        href: string;
        label: string;
    };

    const { href, label }: iCreateObjectProps = $props();
</script>

<button class="btn btn-success gap-2" onclick={() => (window.location.href = href)}>
    <span class="icon-[lucide--circle-plus] size-5"></span>
    {label}
</button>
