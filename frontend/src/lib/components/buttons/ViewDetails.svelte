<script lang="ts">
    type iViewDetailsProps = {
        href: string;
        label?: string | null;
    };

    const { href, label = null }: iViewDetailsProps = $props();
</script>

<a {href} class="btn btn-accent btn-sm"
    ><span class="icon-[lucide--eye] size-4"></span>
    {#if label}{label}{/if}
</a>
