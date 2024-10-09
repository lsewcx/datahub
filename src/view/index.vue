<template>
    <div>
        <Button class="mt-10 ml-10">创建新项目</Button>
        <Card class="w-[300px] mt-10 ml-10">
            <CardHeader>
                <CardTitle>街道目标检测</CardTitle>
                <CardDescription>2024.10.9</CardDescription>
            </CardHeader>
            <CardContent>
                <Badge>目标检测</Badge>
                <p>images  2189</p>
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
</script>