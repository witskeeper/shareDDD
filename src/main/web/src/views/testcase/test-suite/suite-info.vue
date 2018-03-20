<style lang="less">
    @import '../../../styles/common.less';
</style>

<template>
    <div>
        <Col span="6">
            <Card>
                <Tree :data="groupList" @on-check-change="setInterfaceInGroup" show-checkbox ref="tree" style="width:260px"></Tree>
            </Card>
        </Col>
        <Col span="18" class="padding-left-10">
            <Card>
                <div>
                    <Transfer
                        :data="data3"
                        :target-keys="targetKeys3"
                        :list-style="listStyle"
                        :render-format="render3"
                        :operations="['To left','To right']"
                        filterable

                        @on-change="handleChange3">
                        <div :style="{float: 'right', margin: '5px'}">
                            <Button type="ghost" size="small" @click="reloadMockData">Refresh</Button>
                        </div>
                    </Transfer>
                </div>
            </Card>
        </Col>
    </div>
</template>
<script>
import axios  from 'axios';
    export default {
        data () {
            return {
                groupList:[],
                data3: this.getMockData(),
                targetKeys3: this.getTargetKeys(),
                listStyle: {
                    width: '300px',
                    height: '800px'
                },
            }
        },
        methods: {
            getGroupList(){
                axios.get("/v1/group/getGroupByProjectId",{params:{projectId:1,type:1}}).then((res)=>{
                    console.log(res);
                    if(res.data.success){
                        const that =this;
                        res.data.message.forEach(function(item){

                            that.groupList.push(item);
                        });
                    }else{
                        this.$Message.error("获取数据失败")
                    }
                })
            },
            getMockData () {
                let mockData = [];
                for (let i = 1; i <= 20; i++) {
                    mockData.push({
                        key: i.toString(),
                        label: 'Content ' + i,
                        description: 'The desc of content  ' + i,
                        disabled: Math.random() * 3 < 1
                    });
                }
                return mockData;
            },
            getTargetKeys () {
                return this.getMockData()
                        .filter(() => Math.random() * 2 > 1)
                        .map(item => item.key);
            },
            handleChange3 (newTargetKeys) {
                this.targetKeys3 = newTargetKeys;
            },
            render3 (item) {
                return item.label + ' - ' + item.description;
            },
            reloadMockData () {
                this.data3 = this.getMockData();
                this.targetKeys3 = this.getTargetKeys();
            },
            setInterfaceInGroup(){
            }
        },
        created () {
            this.getGroupList();
        },
    }
</script>