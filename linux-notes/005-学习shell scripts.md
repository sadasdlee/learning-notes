# 第 12 章 · 学习 Shell Scripts

> 核心一句话:**Shell Script = 把一串命令写成文件,让 Linux 自动顺序执行。** 本章三大块:① 脚本基础与执行 ② 条件判断(if/case)与循环(for/while)③ 函数与调试。学完你能写出实用的自动化运维脚本。

---

## 一、什么是 Shell Script

### 1. 定义
- Shell Script 是**用 shell 命令写成的程序**,文件里是一连串命令,shell 逐行解释执行。
- 用途:自动化运维、批量处理、定时任务、系统管理。

### 2. 为什么要学
- Linux 系统的服务启动、开机流程几乎都是 shell script;
- 重复操作写成脚本一劳永逸;
- 不需要编译,改完即用,灵活。

### 3. 第一个脚本(标准写法)

```bash
#!/bin/bash
# 这是一个注释
echo "Hello World"
echo "当前用户: $(whoami)"
```

**关键点:**
| 元素 | 说明 |
|------|------|
| `#!/bin/bash` | **shebang**,声明用哪个 shell 解释执行,必须在第一行 |
| `#` 注释 | 除 shebang 外,#开头是注释 |
| `echo` | 输出 |

---

## 二、脚本的编写与执行

### 1. 执行方式(四种)

```bash
# 方式1:赋予执行权限后直接执行(最常用)
chmod +x script.sh
./script.sh

# 方式2:用 bash 直接执行(不需要执行权限)
bash script.sh

# 方式3:用 source 或 . 执行(在当前 shell 环境运行)
source script.sh
. script.sh

# 方式4:sh 执行
sh script.sh
```

### 2. ⭐ 方式区别(重点,易考)

| 执行方式 | 是否需要执行权限 | 是否在子进程中 | 变量是否影响当前 shell |
|----------|------------------|----------------|------------------------|
| `./script.sh` | ✅ 需要 | ✅ 子进程 | ❌ 不影响 |
| `bash script.sh` | ❌ 不需要 | ✅ 子进程 | ❌ 不影响 |
| `source script.sh` | ❌ 不需要 | ❌ 当前 shell | ✅ 影响(变量/函数保留) |

> ⚠️ 关键:`./` 和 `bash` 在**子进程**跑,脚本里 `exit` 不会退出当前终端,定义的变量也不会留下;`source` 在**当前 shell** 跑,变量函数会保留,常用于加载配置文件(如 `source ~/.bashrc`)。

### 3. 良好编写习惯
- 第一行写 shebang;
- 注释说明功能、作者、日期;
- 关键步骤加注释;
- 变量名用大写或清晰命名;
- 复杂逻辑先画流程再写。

---

## 三、简单范例与判断条件

### 1. 交互式脚本(read)

```bash
#!/bin/bash
read -p "请输入你的名字: " name
echo "你好, ${name}!"
```

### 2. 随日期变化(备份脚本经典)

```bash
#!/bin/bash
echo "今天是 $(date +%Y-%m-%d)"
# 备份文件带日期
cp data.txt "data_$(date +%Y%m%d).bak"
```

### 3. 数值运算

```bash
# 方法1:$(( ))
total=$((5 + 3))
echo $total        # 8

# 方法2:declare -i
declare -i n=10+5
echo $n            # 15

# 方法3:expr
echo $(expr 5 \* 3)   # 15 (* 需转义)
```

> 数值运算推荐 `$(( ))`,最简洁,支持 + - * / %。

### 4. ⭐ test 测试命令(条件判断基础)

`test` 用来判断条件真假,返回 0(真)或非0(假)。

```bash
test -e /etc/passwd && echo "存在" || echo "不存在"
# 等价写法:用方括号 [ ]
[ -e /etc/passwd ] && echo "存在" || echo "不存在"
```

**常用判断条件:**

| 类型 | 选项 | 含义 |
|------|------|------|
| 文件类型 | `-e` | 存在 |
| | `-f` | 存在且为文件 |
| | `-d` | 存在且为目录 |
| 文件权限 | `-r` | 可读 |
| | `-w` | 可写 |
| | `-x` | 可执行 |
| 字符串 | `-z str` | 字符串为空 |
| | `-n str` | 字符串非空 |
| | `str1 == str2` | 相等 |
| | `str1 != str2` | 不等 |
| 数值 | `-eq` | 等于 |
| | `-ne` | 不等 |
| | `-gt` / `-lt` | 大于 / 小于 |
| | `-ge` / `-le` | 大于等于 / 小于等于 |

**多条件组合:**
```bash
[ -f file ] && [ -r file ]    # 且(-a 已弃用)
[ -f file ] || [ -d dir ]     # 或(-o 已弃用)
```

> ⚠️ 方括号两侧**必须有空格**:`[ -e file ]` ✅,`[-e file]` ❌。

---

## 四、条件判断语句

### 1. if 语句

```bash
# 基本结构
if [ 条件 ]; then
    命令
fi

# if-else
if [ 条件 ]; then
    命令1
else
    命令2
fi

# if-elif-else
if [ $score -ge 90 ]; then
    echo "A"
elif [ $score -ge 60 ]; then
    echo "B"
else
    echo "C"
fi
```

> 注意:每个分支以 `;` 和 `then` 结尾,最后用 `fi` 闭合。

### 2. case 语句(多分支,比 if-elif 清晰)

```bash
case $1 in
    "start")
        echo "启动服务"
        ;;
    "stop")
        echo "停止服务"
        ;;
    "restart")
        echo "重启服务"
        ;;
    *)
        echo "用法: $0 {start|stop|restart}"
        ;;
esac
```

| 语法 | 说明 |
|------|------|
| `case 变量 in` | 开始 |
| `模式)` | 匹配模式 |
| `;;` | 每个分支结束(类似 break) |
| `*)` | 默认分支(类似 default) |
| `esac` | 结束(case 反过来写) |

> 模式可用通配符:`y*` 匹配 y 开头,`y|Y` 匹配 y 或 Y。

---

## 五、循环语句

### 1. for 循环

```bash
# 写法1:遍历列表
for i in 1 2 3 4 5; do
    echo $i
done

# 写法2:遍历命令结果
for file in $(ls *.txt); do
    echo "处理: $file"
done

# 写法3:C 风格(数值循环)
for ((i=1; i<=5; i++)); do
    echo $i
done

# 写法4:遍历数组
arr=(apple banana cherry)
for fruit in ${arr[@]}; do
    echo $fruit
done
```

### 2. while 循环(条件为真时循环)

```bash
# 基本结构
while [ 条件 ]; do
    命令
done

# 示例:计数
n=1
while [ $n -le 5 ]; do
    echo $n
    n=$((n+1))
done

# 读取文件每行
while read line; do
    echo "行: $line"
done < /etc/passwd
```

### 3. until 循环(条件为假时循环,与 while 相反)

```bash
n=1
until [ $n -gt 5 ]; do
    echo $n
    n=$((n+1))
done
```

### 4. break 与 continue

```bash
for i in 1 2 3 4 5; do
    [ $i -eq 3 ] && continue    # 跳过3
    [ $i -eq 5 ] && break       # 遇到5退出
    echo $i
done
# 输出: 1 2 4
```

### 5. 循环速记

```
for 变量 in 列表; do ... done        遍历
for ((初;条件;步)); do ... done       C风格
while [ 条件 ]; do ... done           条件真循环
until [ 条件 ]; do ... done           条件假循环
break 退出循环 / continue 跳过本次
```

---

## 六、函数

### 1. 定义与调用

```bash
# 定义
function print_hello() {
    echo "Hello $1"        # $1 是函数参数
}

# 调用
print_hello "Tom"          # 输出 Hello Tom
```

### 2. 函数参数与返回值

```bash
add() {
    echo $(($1 + $2))      # $1 $2 是传入参数
}
result=$(add 3 5)          # 用命令替换获取返回值
echo $result               # 8
```

| 要点 | 说明 |
|------|------|
| 函数参数 | `$1 $2 $@` 同脚本参数用法 |
| 返回值 | 用 `echo` 输出 + `$()` 捕获(常用) |
| `return` | 只能返回 0-255 的状态码,不是真正的返回值 |
| 局部变量 | `local var=value`,避免污染全局 |

```bash
# 局部变量示例
counter() {
    local x=10        # 局部,函数外不可见
    echo $x
}
```

---

## 七、脚本调试

### 1. sh 命令的调试选项

```bash
sh -n script.sh     # 语法检查,不执行(检查语法错误)
sh -x script.sh     # 执行并打印每条命令(调试最常用)⭐
sh -v script.sh     # 执行前打印脚本内容
```

### 2. -x 调试示例

```bash
$ sh -x test.sh
+ echo 'Hello World'    # + 开头是实际执行的命令
Hello World
```

> `sh -x` 是排查脚本 bug 的第一工具,能看清每步执行了什么、变量值是什么。

### 3. 常见错误排查

| 现象 | 排查 |
|------|------|
| `command not found` | 命令拼写错、或 PATH 没找到 |
| `syntax error` | 用 `sh -n` 查语法 |
| 变量为空 | 是否忘了 `$`、或变量没传进来 |
| 逻辑不对 | 用 `sh -x` 看执行流程 |

---

## 八、实用脚本范例

### 1. 批量备份

```bash
#!/bin/bash
# 备份指定目录,文件名带日期
BACKUP_DIR="/home/user/data"
DEST="/backup"
DATE=$(date +%Y%m%d)

tar -czf "${DEST}/backup_${DATE}.tar.gz" "$BACKUP_DIR"
echo "备份完成: backup_${DATE}.tar.gz"
```

### 2. 判断服务是否运行

```bash
#!/bin/bash
if pgrep -x "nginx" > /dev/null; then
    echo "nginx 运行中"
else
    echo "nginx 未运行,正在启动..."
    systemctl start nginx
fi
```

### 3. 批量重命名文件

```bash
#!/bin/bash
for file in *.txt; do
    mv "$file" "${file%.txt}.md"
done
echo "全部 .txt 已改为 .md"
```

---

## 九、重点速记清单

1. **第一行 shebang** `#!/bin/bash` 必写。
2. **执行方式**:`./`(要权限,子进程)、`bash`(不要权限,子进程)、`source`(当前 shell,变量保留)。
3. **数值运算**用 `$(( ))`,最简洁。
4. **test/[] 判断**:方括号两侧必须空格;文件 `-e/-f/-d`,数值 `-eq/-gt`,字符串 `-z/-n/==`。
5. **if**:`if;then...elif;then...else...fi`。
6. **case**:`case in 模式) ... ;; *) ... esac`,注意 `;;` 和 `esac`。
7. **循环**:for/while/until,`break`/`continue`。
8. **函数**:`function name() {}`,参数 `$1 $2`,返回值用 echo + `$()`。
9. **调试**:`sh -n` 查语法,`sh -x` 看执行流程(最常用)。
10. **变量替换**:`${var%.*}` 删后缀、`${var#*/}` 删前缀(第10章内容,脚本里常用)。

---

## 十、常见易错点回顾

- ❌ 第一行漏 `#!/bin/bash` → 用 `./` 执行可能用了错误 shell。
- ❌ `./script.sh` 提示 Permission denied → 忘了 `chmod +x`。
- ❌ `[-e file]` 报错 → 方括号没空格,要 `[ -e file ]`。
- ❌ `if [$a -eq 1]` → 变量和括号间也要空格:`if [ $a -eq 1 ]`。
- ❌ 用 `bash` 执行后变量没生效 → 子进程不回传变量,要 `source`。
- ❌ 函数 `return` 想返回字符串 → return 只返回状态码,用 `echo` + `$()`。
- ❌ `$(())` 写成 `$()` → 前者数值运算,后者命令替换,别混。
- ❌ for 循环改不了外部变量 → 检查是否在子 shell(管道里 `| while` 是子 shell),变量要用进程替换或重定向文件。
