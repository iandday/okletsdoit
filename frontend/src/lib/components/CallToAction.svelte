<script lang="ts">
    type ICallToAction = {
        title?: string;
        content?: string;
    };

    const { title, content }: ICallToAction = $props();
</script>

<div class="text-center mt-16 md:mt-20 lg:mt-24 transition-all duration-1000 starting:opacity-0 starting:blur-sm">
    <div class="card bg-base-100 text-secondary-content shadow-2xl border border-primary/20 max-w-3xl mx-auto">
        <div class="card-body items-center text-center">
            <div class="flex flex-row gap-4 items-center justify-center mb-4">
                <span class="text-accent iconify lucide--heart size-12"></span>
                <h3 class=" text-2xl md:text-3xl font-bold">{title}</h3>
            </div>
            <p class=" text-md leading-relaxed">
                {content}
            </p>
        </div>
    </div>
</div>
