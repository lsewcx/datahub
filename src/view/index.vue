<template>
    <div>
        <Button class="mt-10 ml-10">创建新项目</Button>
        <Card class="w-[300px] mt-10 ml-10">
            <CardHeader>
                <CardTitle>{{ data.name }}</CardTitle>
                <CardDescription>{{ data.date }}</CardDescription>
            </CardHeader>
            <CardContent>
                <Badge>{{ data.badge }}</Badge>
                <p>images {{ data.totals }}</p>
            </CardContent>
        </Card>
    </div>
</template>

<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card'
import { index } from "../types/index"

// 定义数据对象
const data: index = {
    id: 1,
    name: '街道目标检测',
    date: Date.now(),
    badge: '目标检测',
    totals: 2189
}

</script>