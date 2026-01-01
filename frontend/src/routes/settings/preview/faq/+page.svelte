<script>
    import Faq from "$lib/components/Faq.svelte";
    import PageShell from "$lib/components/layouts/PageShell.svelte";

    const { data } = $props();
</script>

<div>
    <PageShell title="Frequently Asked Questions">
        <Faq categories={data.categories} preview={true} />
    </PageShell>
</div>
