## 统一管理session_state初始化工作

### 1. 分析当前问题
- 项目已有`utils/state_manager.py`文件，定义了`DEFAULT_SESSION_STATE`和相关管理函数
- 但在`home.py`和多个视图文件中仍直接操作`st.session_state`
- 缺少在应用启动时统一调用初始化函数的机制
- 部分session_state变量可能未在`DEFAULT_SESSION_STATE`中定义

### 2. 优化方案

#### 步骤1：在home.py中添加session_state初始化调用
- 在`home.py`文件顶部导入`state_manager`
- 在应用启动时调用`init_session_state()`函数
- 目的：确保所有session_state变量在应用启动时被统一初始化

#### 步骤2：完善DEFAULT_SESSION_STATE定义
- 检查所有直接使用的session_state变量
- 确保`DEFAULT_SESSION_STATE`中包含所有需要的变量
- 目的：避免在代码中直接初始化新的session_state变量

#### 步骤3：修改home.py中的button_submit函数
- 替换直接操作`st.session_state`的代码
- 使用`state_manager`中的函数来管理状态
- 目的：统一状态管理方式，避免散落在各处的初始化代码

#### 步骤4：修改其他视图文件
- 逐步替换其他视图文件中直接操作`st.session_state`的代码
- 改为使用`state_manager`中提供的接口
- 目的：确保所有状态操作都通过统一的管理接口进行

### 3. 预期效果
- session_state的初始化工作被统一管理
- 所有session_state变量在应用启动时被初始化
- 避免了在各处散落地初始化session_state变量
- 提高了代码的可维护性和一致性

### 4. 实施顺序
按照上述步骤依次实施，每次只修改一个文件，确保改动是原子的，并且修改后程序可以正常运行。