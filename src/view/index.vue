<template>
    <div>
        <Button class="mt-10 ml-14">创建新项目</Button>
        <div class="flex flex-wrap mt-1 ml-10">
            <div v-for="item in data" :key="item.id" class="m-4">
                <Card class="w-[300px]">
                    <CardHeader>
                        <CardTitle>{{ item.name }}
                            <DropdownMenu>
                                <DropdownMenuTrigger as-child>
                                    <Button variant="outline" class="p-2 ml-36">
                                        <MoreHorizontal class="h-4 w-4" />
                                    </Button>
                                </DropdownMenuTrigger>
                                <DropdownMenuContent class="w-56">
                                    <DropdownMenuItem>
                                        <Trash class="mr-2 h-4 w-4" />
                                        <span>删除项目</span>
                                    </DropdownMenuItem>
                                </DropdownMenuContent>
                            </DropdownMenu>
                        </CardTitle>
                        <CardDescription>{{ item.date }}</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <Badge>{{ item.badge }}</Badge>
                        <p>images {{ item.totals }}</p>
                    </CardContent>
                </Card>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getProjects } from '@/api/index'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card'
import {
    MoreHorizontal,
    Trash,
} from 'lucide-vue-next'
import { project } from '../types/index'

const data = ref<project[]>([])

onMounted(() => {
    getProjects().then((res) => {
        data.value = res.data
    })
})
</script>