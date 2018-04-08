<style lang="less">
@import "../../styles/common.less";
@import "./components/table.less";
@import "./dbdoc-list-info.less";
</style>

<template>
    <div>
        <Row>
            <!-- <Card> -->
            
            <Col span="18">
                <div class="margin-top-10">
                    <Select v-model="searchInput" placeholder="搜索表名(user) / 表字段(user.id) / 字段(.id)" 
                     filterable remote :remote-method="remoteSearch" :loading="selectIsLoading" clearable @on-change="selectChange">
                        <Option v-for="item in searchList" :value="item.id" :key="item.uid">{{item.eName}}</Option>
                    </Select>
                </div>
                <div class="margin-top-10">
                    <div style="font-size:25px">  {{tableDataModel.eName}}（<span v-if="cNameEditIsHide">{{tableDataModel.cName}}</span>
                    <Input  v-if="!cNameEditIsHide" v-model="tableDataModel.cName" icon="checkmark" 
                    style="width: 200px" @on-click="editTableCNameByName"></Input>）
                        <Button  v-if="cNameEditIsHide" type="ghost" shape="circle" icon="edit"  size="small" 
                        @click="ChangeEditTableShow"></Button>
                        <Button type="success" @click="setCloumnLink"  size="small" >增加外键/数据关系</Button>
                    </div>
                </div>
                <div class="margin-top-10">
                <Collapse v-model="collapseStatus" accordion >
                  <Panel name="1">
                      数据流
                      <div slot="content">
                        <Timeline v-for="item in routeList">
                            <TimelineItem v-for="r in item.route"  color="green">
                              <p class="time">{{r.data_operation}}</p>
                              <p class="content">{{r.data_module}}</p>
                            </TimelineItem>
                        </Timeline>
                      </div>
                  </Panel>
                  <Panel name="2">
                      外键/数据关系
                      <div slot="content">
                        <p>tree：http://echarts.baidu.com/examples/editor.html?c=tree-legend</p>
                        <p>sandkey:http://echarts.baidu.com/examples/editor.html?c=sankey-energy</p>
                      </div>
                  </Panel>
                </Collapse>
                </div>
                <div class="margin-top-10">    
                    <Input v-model="tableDataModel.remark" type="textarea" :autosize="{minRows: 2,maxRows: 5}" 
                    placeholder="备注" @on-blur="editTableByNameNet"></Input>
                </div>
                
                <div class="edittable-table-height-con margin-top-10">
                    <can-edit-table border :columns-list="listColumn" v-model="listData"
                    :hover-show="true" :edit-incell="true" @on-cell-change="handleCellChange" 
                    @on-cell-link="handleLinkGo" ></can-edit-table>
                </div>
                
            </Col>
            <Col span="6" class="padding-left-10">
                <div class="">
                    <Card>
                        <p slot="title">
                            <Icon type="navicon-round"></Icon>
                            【{{groupRelation.dbName}}】文档目录
                        </p>
                        <Tree ref="tree" :data="groupRelation.groupInfo" @on-select-change="getTreeTableInfo"></Tree>
                    </Card>
                </div>
                
            </Col>
        <!-- </Card> -->
        </Row>
    <Modal v-model="setLinkModal" title="增加外键/数据关系" @on-ok="addColumnLink">
        <!-- todo 枚举值先写死了 -->
        <div class="margin-top-10">
          关系类型
          <Select v-model="selectLinkType" style="width:200px">
              <!-- <Option v-for="item in listData" :value="item.id" :key="item.id">{{ item.name }}</Option> -->
              <Option :value="0" :key="0">外键关系</Option>
              <Option :value="1" :key="1">数据关系</Option>
          </Select>
        </div>
        <div class="margin-top-10">
          源字段
          <Select v-model="selectSrcColumn" style="width:200px">
              <Option v-for="item in listData" :value="item.id" :key="item.id">{{ item.eName }}</Option>
          </Select>
        </div>
        <div class="margin-top-10">
          关系库
          <Select v-model="selectLinkDB" style="width:200px" @on-change="selectLinkDBChange">
              <Option v-for="item in linkDBList" :value="item.id" :key="item.id">{{ item.name }}</Option>
          </Select>
        </div>
        <div class="margin-top-10">
            <!-- 默认选取已经产生关联的，否则选取条件下的，支持跨库 -->
            关系表
          <Select v-model="selectLinkTable" style="width:200px" @on-change="selectLinkTableChange" 
           filterable remote :remote-method="remoteLinkTableSearch" :loading="selectIsLoading">
              <Option v-for="item in linkTableList" :value="item.id" :key="item.id">{{ item.eName }}</Option>
          </Select>
        </div>
        <div class="margin-top-10">
            <!-- 默认选取已经产生关联的，否则选取条件下的，支持跨库 -->
          关系字段
          <Select v-model="selectLinkColumn" style="width:200px" @on-change="selectLinkColumnChange" 
           filterable remote :remote-method="remoteLinkColumnSearch" :loading="selectIsLoading">
              <Option v-for="item in linkColumnList" :value="item.id" :key="item.id">{{ item.eName }}</Option>
          </Select>
        </div>
    </Modal>
    </div>
</template>

<script>
import canEditTable from "./components/canEditTable.vue";
import axios from "axios";
export default {
  name: "dbdoc-list-info",
  components: {
    canEditTable
  },
  data() {
    return {
        selectSrcColumn: "",
        selectLinkType: "",
        linkDBList: [],
        selectLinkDB: "",
        linkTableList: [],
        selectLinkTable: "",
        linkColumnList: [],
        selectLinkColumn: "",
        setLinkModal: false,
        collapseStatus: "",
        selectIsLoading: false,
        treeTableName: "",
        listColumn: [
            {
            title: "字段",
            width: 120,
            key: "eName"
            },
            {
            title: "类型",
            width: 120,
            key: "type"
            },
            {
            title: "备注",
            key: "remark",
            editable: true
            },
            {
            title: "外键/数据关系",
            width: 170,
            key: "links",
            showlink: true
            },
            {
            title: "废弃",
            width: 120,
            key: "is_discarded",
            editable: true
            }
        ],
        listData: [],
        tableDataModel: {
            id: 0,
            eName: "",
            cName: "",
            type: "",
            remark: "",
            is_discarded: 0
        },
        groupRelation: {
            dbName: "",
            groupInfo: []
        },
        DBId: 0,
        cNameEditIsHide: true,
        searchInput: "",
        searchList: [],
        searchList1: [],
        columnLinkModel: {
        　  src_column_id: 0,
        　  src_table_id: 0,
        　  relation_type: 0,
        　  link_column_id: 0,
        　  link_table_id: 0,
        },
        routeList: []
    };
  },
  methods: {
    initColumnDataModel() {
      this.tableDataModel = {
        id: 0,
        eName: "",
        cName: "",
        type: "",
        remark: "",
        is_discarded: 0
      };
    },
    initcolumnLinkModel() {
        this.columnLinkModel = {
            src_column_id: 0,
            src_table_id: 0,
            relation_type: 0,
            link_column_id: 0,
            link_table_id: 0,
        };
    },
    getData() {
      // console.log(this.$route)
      this.DBId = this.$route.query.id;
      this.isSearch=0;
      this.getTableGroupRelationListNet();
           setInterval(()=>{
              this.isSearch++;
          },500);
    },
    getTableRouteListtNet(table_id) {
      axios
        .get("/v1/table/getTableRouteList", {
          params: { id: table_id }
        })
        .then(res => {
          if (res.data.success) {
              this.routeList = res.data.message
            return res.data.message;
          } else {
            this.$Message.error("失败");
          }
        });
    },
    getTableGroupRelationListNet() {
      axios
        .get("/v1/database/getTableGroupRelationList", {
          params: { id: this.DBId }
        })
        .then(res => {
          if (res.data.success) {
            // debugger
            this.groupRelation = res.data.message;
            let tableId = this.groupRelation.groupInfo[0].children[0].tableId;
            this.getColumnListByTableIdNet(tableId);
            this.getTableInfoByIdNet(tableId)
            // this.routeList = this.getTableRouteListtNet(tableId)
            this.getTableRouteListtNet(tableId)
            console.log(this.routeList)
          } else {
            this.$Message.error("失败");
          }
        });
    },
    getTreeTableInfo(selectedArray) {
      let isHasChildren = selectedArray[0].children;
      let id = 0
      // todo 根节点不要选中且没有事件
      if (Array.isArray(isHasChildren)) {
        selectedArray[0].selected = false;
      } else {
        id = selectedArray[0].tableId;
        this.getColumnListByTableIdNet(id);
        this.getTableInfoByIdNet(id);
      }
    },
    getColumnListByTableNameNet(tableName) {
      axios
        .post("/v1/table/getColumnListByTableName", {
          DBId: this.DBId,
          eName: tableName
        })
        .then(res => {
          if (res.data.success) {
            this.listData = res.data.message;
          } else {
            this.$Message.error("失败");
          }
        });
    },
    getTableInfoByNameNet(tableName) {
      axios
        .post("/v1/table/getTableInfoByName", {
          DBId: this.DBId,
          eName: tableName
        })
        .then(res => {
          if (res.data.success) {
            this.tableDataModel = res.data.message[0];
          } else {
            this.$Message.error("失败");
          }
        });
    },
    getColumnListByTableIdNet(tableId) {
        this.columnLinkModel.src_table_id = tableId
        axios
        .get("/v1/table/getColumnListByTableId", {
          params: { id: tableId}
        })
        .then(res => {
          if (res.data.success) {
            this.listData = res.data.message;
          } else {
            this.$Message.error("失败");
          }
        });
    },
    getTableInfoByIdNet(tableId) {
      axios
        .get("/v1/table/getTableInfoById", {
          params: { id: tableId}
        })
        .then(res => {
          if (res.data.success) {
            this.tableDataModel = res.data.message[0];
          } else {
            this.$Message.error("失败");
          }
        });
    },
    handleCellChange(val, index, key) {
      if (key === "is_discarded") {
        this.editColumnDiscardByIdNet(
          val[index][key],
          parseInt(val[index]["id"]),
          key
        );
      } else if (key === "remark") {
        this.editColumnRemarkByIdNet(val[index][key], val[index]["id"], key);
      }
    },
    handleLinkGo(val, index, key, id) {
      console.log(id)
      this.getColumnListByTableIdNet(id)
      this.getTableInfoByIdNet(id)
      this.changeTreeSelected(id)

    },
    editColumnRemarkByIdNet(val, index, key) {
      axios
        .post("/v1/table/editColumnRemarkById", {
          id: index,
          key: key,
          val: val
        })
        .then(res => {
          if (res.data.success) {
            this.$Message.success("编辑成功");
          } else {
            this.$Message.error("失败");
          }
        });
    },
    editColumnDiscardByNameNet(val, index, key) {
      axios
        .post("/v1/table/editColumnDiscardById", {
          id: index,
          key: key,
          val: val
        })
        .then(res => {
          if (res.data.success) {
            this.$Message.success("编辑成功");
          } else {
            this.$Message.error("失败");
          }
        });
    },
    editTableByNameNet() {
      axios.post("/v1/table/editTableByName", this.tableDataModel).then(res => {
        if (res.data.success) {
          this.$Message.success("编辑成功");
        } else {
          this.$Message.error("失败");
        }
      });
    },
    editTableCNameByName() {
      this.ChangeEditTableShow();
      this.editTableByNameNet();
    },
    ChangeEditTableShow() {
      this.cNameEditIsHide = !this.cNameEditIsHide;
    },
    remoteSearch(query) {
      if(this.isSearch%3!=0){
        return;
      }
      var index = query.indexOf(".");
      var content = { DBId: this.DBId, content: query };
      if(content != "") {
        if (index > 0) {
          // table.column
          this.getSearchList(0, content);
        } else if (index == -1) {
          // table
          this.getSearchList(1, content);
        } else if (index == 0) {
          // .column
          this.getSearchList(2, content);
        }
      }
      
    },
    getSearchList(searchType, content) {
      if (searchType == 0) {
        // table.column
        this.selectIsLoading = true;
        axios.post("/v1/table/getSearchByTableColumn", content).then(res => {
          if (res.data.success) {
            // this.$Message.success("成功");
            this.searchList = res.data.message;
            this.selectIsLoading = false;
          } else {
            this.$Message.error("失败");
          }
        });
      } else if (searchType == 1) {
        // table
        this.selectIsLoading = true;
        axios.post("/v1/table/getSearchByTable", content).then(res => {
          if (res.data.success) {
            //  this.$Message.success("成功");
            this.searchList = res.data.message;
            this.selectIsLoading = false;
          } else {
            this.$Message.error("失败");
          }
        });
      } else if (searchType == 2) {
        // .column
        this.selectIsLoading = true;
        axios.post("/v1/table/getSearchByColumn", content).then(res => {
            if (res.data.success) {
                // this.$Message.success("成功");
                this.searchList = res.data.message;
                this.selectIsLoading = false;
            } else {
                this.$Message.error("失败");
            }
        });
      }
    },
    selectChange(val) {
        var id = val
        if(id > 0) {
          this.getColumnListByTableIdNet(id);
          this.getTableInfoByIdNet(id);
          this.changeTreeSelected(id)
        }
        
    },
    changeTreeSelected(id) {
      this.groupRelation.groupInfo.forEach(grops =>{
        grops.children.forEach(item =>{
          if(item.id==id){
            this.$set(item,'selected',true);
          }else{
            this.$set(item,'selected',false);
          }
        })
      })
    },
    addColumnLink() {
      this.setLinkModal = false
      this.columnLinkModel.relation_type = this.selectLinkType
      this.columnLinkModel.link_table_id = this.selectLinkTable
      this.columnLinkModel.link_column_id = this.selectLinkColumn
      this.columnLinkModel.src_column_id = this.selectSrcColumn
      this.addColumnLinkNet()
    },
    addColumnLinkNet() {
        axios.post("/v1/table/addColumnLink",
            this.columnLinkModel
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getData();

                }else{
                    this.$Message.error("失败")
                }
            }
            )
            this.initColumnLinkModel()
            this.selectLinkTable = ""
            this.selectLinkColumn = ""
            this.selectLinkDB = ""
            this.selectSrcColumn = ""
            this.selectLinkType = ""
    },
    setCloumnLink() {
        this.setLinkModal = true
        this.getDatabaseListNet()

    },
    getDatabaseListNet() {
        // todo id写死了
        return axios.get("/v1/database/getDatabaseList",
        {"params":{"id": 2}}).then((res)=>{
            if(res.data.success){
                this.linkDBList = res.data.message;
                // return res
            }else{
                this.$Message.error("失败")
            }
        }
        )
    },
    getLinkTableListNet(id) {
        return axios.get("/v1/table/getLinkTableList",
        {"params":{"id": id}}).then((res)=>{
            if(res.data.success){
                this.linkTableList = res.data.message;
            }else{
                this.$Message.error("失败")
            }
        }
        )
    },
    getLinkColumnListNet(id) {
        return axios.get("/v1/table/getLinkColumnList",
        {"params":{"id": id}}).then((res)=>{
            if(res.data.success){
                this.linkColumnList = res.data.message;
            }else{
                this.$Message.error("失败")
            }
        }
        )
    },
    selectLinkDBChange(val) {
        // todo selectLinkTable?
        this.getLinkTableListNet(val)
        this.selectLinkTable = ""
        this.selectLinkColumn = ""        
    },
    selectLinkTableChange(val) {
        this.getLinkColumnListNet(val)
        this.selectLinkColumn = ""
    },
    selectLinkColumnChange() {
        
    },
    remoteLinkTableSearch(query) {
        this.selectIsLoading = true;
        axios.post("/v1/table/getTableListByTableName", {
          id: this.selectLinkDB,
          content: query
        }).then(res => {
          if (res.data.success) {
            // this.$Message.success("成功");
            this.linkTableList = res.data.message;
            this.selectIsLoading = false;
          } else {
            this.$Message.error("失败");
          }
        });
    },
    remoteLinkColumnSearch(query) {
        this.selectIsLoading = true;
        axios.post("/v1/table/getColumnListByColName", {
          id: this.selectLinkTable,
          content: query
        }).then(res => {
          if (res.data.success) {
            // this.$Message.success("成功");
            this.linkColumnList = res.data.message;
            this.selectIsLoading = false;
          } else {
            this.$Message.error("失败");
          }
        });
    },
  },
  created() {
    this.getData();
  }
};
</script>
