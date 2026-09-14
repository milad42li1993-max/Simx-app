import os

def write(path, content):
    # اصلاح مسیر: فقط اگر نام پوشه خالی نبود آن را بساز
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# 1. settings.gradle.kts
write("settings.gradle.kts", """
pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal() }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories { google(); mavenCentral() }
}
rootProject.name = "SIMX"
include(":app")
""")

# 2. build.gradle.kts (root)
write("build.gradle.kts", """
plugins {
    id("com.android.application") version "8.2.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.22" apply false
}
""")

# 3. gradle.properties
write("gradle.properties", """
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
""")

# 4. app/build.gradle.kts
write("app/build.gradle.kts", """
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}
android {
    namespace = "com.simx.app"
    compileSdk = 34
    defaultConfig {
        applicationId = "com.simx.app"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"
    }
    buildTypes { release { isMinifyEnabled = false } }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
    buildFeatures { compose = true }
    composeOptions { kotlinCompilerExtensionVersion = "1.5.8" }
    packaging { resources { excludes += "/META-INF/{AL2.0,LGPL2.1}" } }
}
dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    implementation("androidx.activity:activity-compose:1.8.2")
    implementation(platform("androidx.compose:compose-bom:2024.02.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    implementation("com.google.code.gson:gson:2.10.1")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
}
""")

# 5. AndroidManifest.xml
write("app/src/main/AndroidManifest.xml", """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <application
        android:allowBackup="true"
        android:label="SIMX"
        android:supportsRtl="true"
        android:theme="@style/Theme.SIMX"
        android:usesCleartextTraffic="true">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
""")

# 6. strings.xml
write("app/src/main/res/values/strings.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">SIMX</string>
</resources>
""")

# 7. themes.xml
write("app/src/main/res/values/themes.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.SIMX" parent="android:Theme.Material.NoActionBar">
        <item name="android:statusBarColor">#0D1117</item>
        <item name="android:navigationBarColor">#0D1117</item>
        <item name="android:windowBackground">#0D1117</item>
    </style>
</resources>
""")

# 8. MainActivity.kt
write("app/src/main/java/com/simx/app/MainActivity.kt", r"""
package com.simx.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

val BG = Color(0xFF0D1117)
val CARD = Color(0xFF161B22)
val GOLD = Color(0xFFD4AF37)
val GRN = Color(0xFF00C853)
val RED = Color(0xFFFF1744)
val BLU = Color(0xFF58A6FF)
val TXT = Color(0xFFE6EDF3)
val SUB = Color(0xFF8B949E)
val BRD = Color(0xFF30363D)

data class T(val sym:String,val pr:String,val ch:String,val up:Boolean,
val bias:String,val bc:Color,val conf:Int,val nar:String,
val sc:String,val alt:String,val act:String,val ac:Color,
val ent:String,val sl:String,val tp:String,val rr:String)

val D = listOf(
T("BTC/USDT","$67,450","+3.4%",true,"صعودی قدرتمند",GRN,85,
"بیت‌کوین پس از جمع‌آوری نقدینگی کف ۶۶,۲۰۰ دلار، با جذب شدید سفارشات فروش مواجه شده. ساختار آماده جهش به ۶۹,۲۰۰ است.",
"پولبک به ۶۶,۹۰۰ ➔ تأیید ➔ پرواز تا ۶۹,۲۰۰",
"شکست ۶۵,۸۰۰ ➔ ریزش تا ۶۴,۲۰۰",
"خرید (LONG)",GRN,"$66,900-$67,100","$65,800","$69,200","1:2.2"),
T("XAU/USD","$2,340","+0.8%",true,"صبر و پایش",BLU,52,
"طلا در محدوده ۲,۳۲۰ تا ۲,۳۵۰ در نوسان است. نشست FOMC فردا جهت بعدی را مشخص می‌کند.",
"انتظار برای FOMC ➔ واکنش به نرخ بهره",
"شکست ۲,۳۵۰ ➔ حرکت تا ۲,۳۸۰",
"صبر کنید",BLU,"-","-","-","-"),
T("EUR/USD","1.0820","-0.6%",false,"نزولی",RED,72,
"یورو تحت فشار داده‌های ضعیف PMI اروپا و تقویت دلار. ساختار LH-LL تأیید شده.",
"پولبک به ۱.۰۸۵۰ ➔ ریزش تا ۱.۰۷۵۰",
"شکست ۱.۰۹۰۰ ➔ صعود تا ۱.۰۹۸۰",
"فروش (SHORT)",RED,"1.0840-1.0860","1.0910","1.0750","1:1.8")
)

class MainActivity : ComponentActivity() {
    override fun onCreate(s: Bundle?) { super.onCreate(s); setContent { App() } }
}

@Composable
fun App() {
    var tab by remember { mutableIntStateOf(0) }
    var si by remember { mutableIntStateOf(0) }
    Column(Modifier.fillMaxSize().background(BG)) {
        Row(Modifier.fillMaxWidth().padding(16.dp),
            Arrangement.SpaceBetween, Alignment.CenterVertically) {
            Text("SIMX AIOS", color=GOLD, fontSize=20.sp, fontWeight=FontWeight.Black)
            Row(verticalAlignment=Alignment.CenterVertically) {
                Text("● زنده", color=GRN, fontSize=12.sp)
                Spacer(Modifier.width(12.dp))
                Text("🔔", fontSize=18.sp)
            }
        }
        Row(Modifier.fillMaxWidth().padding(horizontal=16.dp,vertical=4.dp)
            .clip(RoundedCornerShape(8.dp)).background(Color(0x33FF1744)).padding(10.dp)) {
            Text("⚠️ ۲ ساعت تا نشست FOMC فدرال رزرو — نوسان بالا",
                color=Color(0xFFFF80AB), fontSize=12.sp)
        }
        LazyRow(Modifier.padding(vertical=10.dp),
            contentPadding=PaddingValues(horizontal=16.dp),
            horizontalArrangement=Arrangement.spacedBy(8.dp)) {
            items(D.size) { i ->
                Text(D[i].sym, color=if(i==si) Color(0xFF0D1117) else SUB,
                    fontSize=13.sp, fontWeight=FontWeight.Bold,
                    modifier=Modifier.clip(RoundedCornerShape(20.dp))
                        .background(if(i==si) GOLD else CARD)
                        .clickable { si=i }
                        .padding(horizontal=14.dp, vertical=8.dp))
            }
        }
        Box(Modifier.weight(1f).padding(16.dp)) {
            when(tab) {
                0 -> Dash(D[si])
                1 -> Events()
                2 -> Chat()
                3 -> Settings()
            }
        }
        Row(Modifier.fillMaxWidth().background(CARD).padding(vertical=10.dp),
            Arrangement.SpaceEvenly) {
            listOf("📊 داشبورد","📅 رویدادها","🤖 چت","⚙️ تنظیمات").forEachIndexed { i,l ->
                Text(l, color=if(i==tab) GOLD else SUB, fontSize=11.sp,
                    fontWeight=if(i==tab) FontWeight.Bold else FontWeight.Normal,
                    modifier=Modifier.clickable { tab=i })
            }
        }
    }
}

@Composable
fun Dash(d: T) {
    LazyColumn(verticalArrangement=Arrangement.spacedBy(12.dp)) {
        item {
            Card(colors=CardDefaults.cardColors(containerColor=CARD),
                shape=RoundedCornerShape(18.dp)) {
                Column(Modifier.padding(16.dp)) {
                    Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween) {
                        Column {
                            Text(d.sym, color=TXT, fontSize=20.sp, fontWeight=FontWeight.Bold)
                            Text("تایم‌فریم: 4H", color=SUB, fontSize=11.sp)
                        }
                        Column(horizontalAlignment=Alignment.End) {
                            Text(d.pr, color=if(d.up) GRN else RED, fontSize=18.sp, fontWeight=FontWeight.Bold)
                            Text(d.ch, color=if(d.up) GRN else RED, fontSize=12.sp)
                        }
                    }
                    Spacer(Modifier.height(10.dp))
                    Surface(color=d.bc.copy(alpha=0.15f), shape=RoundedCornerShape(8.dp)) {
                        Text("🎯 ${d.bias} | اطمینان: ${d.conf}%",
                            color=d.bc, fontSize=14.sp, fontWeight=FontWeight.Bold,
                            modifier=Modifier.padding(horizontal=12.dp, vertical=6.dp))
                    }
                    Spacer(Modifier.height(10.dp))
                    Text("📖 داستان بازار:", color=GOLD, fontSize=12.sp, fontWeight=FontWeight.Bold)
                    Text(d.nar, color=SUB, fontSize=13.sp, lineHeight=20.sp)
                    Spacer(Modifier.height(8.dp))
                    HorizontalDivider(color=BRD)
                    Spacer(Modifier.height(8.dp))
                    Text("🎯 سناریوی اصلی:", color=GOLD, fontSize=12.sp)
                    Text(d.sc, color=TXT, fontSize=12.sp)
                    Spacer(Modifier.height(6.dp))
                    Text("🔄 جایگزین:", color=SUB, fontSize=12.sp)
                    Text(d.alt, color=SUB, fontSize=12.sp)
                }
            }
        }
        if (d.act != "صبر کنید") {
            item {
                Card(colors=CardDefaults.cardColors(containerColor=CARD),
                    shape=RoundedCornerShape(18.dp)) {
                    Column(Modifier.padding(16.dp)) {
                        Text("💰 ${d.act}", color=d.ac, fontSize=16.sp, fontWeight=FontWeight.Bold)
                        Spacer(Modifier.height(8.dp))
                        Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween) {
                            Column { Text("ورود",color=SUB,fontSize=11.sp); Text(d.ent,color=TXT,fontSize=13.sp) }
                            Column { Text("حد ضرر",color=SUB,fontSize=11.sp); Text(d.sl,color=RED,fontSize=13.sp) }
                        }
                        Spacer(Modifier.height(6.dp))
                        Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween) {
                            Column { Text("تارگت",color=SUB,fontSize=11.sp); Text(d.tp,color=GRN,fontSize=13.sp) }
                            Column { Text("R:R",color=SUB,fontSize=11.sp); Text(d.rr,color=GOLD,fontSize=13.sp) }
                        }
                        Spacer(Modifier.height(12.dp))
                        Button(onClick={}, Modifier.fillMaxWidth().height(48.dp),
                            colors=ButtonDefaults.buttonColors(containerColor=GOLD),
                            shape=RoundedCornerShape(12.dp)) {
                            Text("🚀 تأیید و اجرای معامله", color=Color(0xFF0D1117), fontWeight=FontWeight.Bold)
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun Events() {
    val ev = listOf(
        Triple("تصمیم نرخ بهره FOMC","🇺🇸 آمریکا • ۲۱:۳۰",5),
        Triple("سخنرانی پاول","🇺🇸 آمریکا • ۲۲:۰۰",5),
        Triple("گزارش اشتغال NFP","🇺🇸 آمریکا • ۱۶:۰۰",5),
        Triple("داده تورم CPI","🇺🇸 آمریکا • ۱۶:۰۰",4),
        Triple("تصمیم نرخ بهره ECB","🇪🇺 اروپا • ۱۵:۱۵",4),
        Triple("تصمیم نرخ بهره BOJ","🇯🇵 ژاپن • ۰۳:۰۰",4),
        Triple("PMI تولید چین","🇨🇳 چین • ۰۴:۳۰",3),
        Triple("تصمیم نرخ بهره BOE","🇬🇧 انگلیس • ۱۴:۰۰",4),
        Triple("تنش ژئوپلیتیک خاورمیانه","🌍 جهانی • فعال",5)
    )
    LazyColumn(verticalArrangement=Arrangement.spacedBy(8.dp)) {
        item { Text("📅 تقویم رویدادهای کلان", color=GOLD, fontSize=20.sp, fontWeight=FontWeight.Bold) }
        items(ev) { (t,info,imp) ->
            val c = if(imp>=5) RED else if(imp>=4) GOLD else BLU
            Card(colors=CardDefaults.cardColors(containerColor=CARD), shape=RoundedCornerShape(12.dp)) {
                Row(Modifier.padding(12.dp), verticalAlignment=Alignment.CenterVertically) {
                    Box(Modifier.width(4.dp).height(40.dp).clip(RoundedCornerShape(2.dp)).background(c))
                    Spacer(Modifier.width(10.dp))
                    Column(Modifier.weight(1f)) {
                        Text(t, color=TXT, fontSize=14.sp, fontWeight=FontWeight.SemiBold)
                        Text(info, color=SUB, fontSize=11.sp)
                    }
                    Surface(color=c.copy(alpha=0.15f), shape=RoundedCornerShape(6.dp)) {
                        Text("$imp/5", color=c, fontSize=12.sp, fontWeight=FontWeight.Bold,
                            modifier=Modifier.padding(6.dp))
                    }
                }
            }
        }
    }
}

@Composable
fun Chat() {
    var inp by remember { mutableStateOf("") }
    val msgs = remember { mutableStateListOf(
        Pair(false,"سلام! من دستیار هوشمند SIMX هستم. ۲۱ سنسور بازار در خدمت شماست.")
    )}
    Column(Modifier.fillMaxSize()) {
        Text("🤖 چت با مغز سیستم", color=GOLD, fontSize=18.sp, fontWeight=FontWeight.Bold)
        Spacer(Modifier.height(10.dp))
        LazyColumn(Modifier.weight(1f), verticalArrangement=Arrangement.spacedBy(8.dp)) {
            items(msgs) { (u,t) ->
                Surface(
                    color=if(u) GOLD else CARD,
                    shape=RoundedCornerShape(12.dp),
                    modifier=Modifier.fillMaxWidth(0.85f)
                        .align(if(u) Alignment.End else Alignment.Start)
                ) {
                    Text(t, color=if(u) Color(0xFF0D1117) else TXT,
                        fontSize=13.sp, modifier=Modifier.padding(10.dp))
                }
            }
        }
        Row(verticalAlignment=Alignment.CenterVertically) {
            TextField(value=inp, onValueChange={inp=it},
                placeholder={Text("سوال خود را بپرسید...",color=SUB)},
                colors=TextFieldDefaults.colors(
                    focusedContainerColor=CARD, unfocusedContainerColor=CARD,
                    focusedTextColor=TXT),
                modifier=Modifier.weight(1f).clip(RoundedCornerShape(12.dp)))
            Spacer(Modifier.width(8.dp))
            Button(onClick={
                if(inp.isNotBlank()) {
                    msgs.add(Pair(true,inp))
                    msgs.add(Pair(false,"تحلیل سنسورها: ساختار صعودی، دلتای خرید مثبت. FOMC نزدیک است، صبر توصیه می‌شود."))
                    inp=""
                }
            }, colors=ButtonDefaults.buttonColors(containerColor=GOLD),
                shape=RoundedCornerShape(12.dp)) {
                Text("ارسال", color=Color(0xFF0D1117))
            }
        }
    }
}

@Composable
fun Settings() {
    Column(verticalArrangement=Arrangement.spacedBy(12.dp)) {
        Text("⚙️ تنظیمات", color=GOLD, fontSize=20.sp, fontWeight=FontWeight.Bold)
        Card(colors=CardDefaults.cardColors(containerColor=CARD), shape=RoundedCornerShape(14.dp)) {
            Row(Modifier.fillMaxWidth().padding(16.dp), Arrangement.SpaceBetween) {
                Text("زبان", color=TXT, fontSize=15.sp)
                Text("فارسی 🇮🇷", color=GOLD, fontSize=14.sp, fontWeight=FontWeight.Bold)
            }
        }
        Card(colors=CardDefaults.cardColors(containerColor=CARD), shape=RoundedCornerShape(14.dp)) {
            Column(Modifier.padding(16.dp)) {
                Text("وضعیت سرور", color=TXT, fontSize=15.sp)
                Text("🟢 آنلاین — فرانکفورت، آلمان", color=GRN, fontSize=13.sp)
                Text("۲۱ سنسور فعال", color=SUB, fontSize=12.sp)
            }
        }
        Card(colors=CardDefaults.cardColors(containerColor=CARD), shape=RoundedCornerShape(14.dp)) {
            Column(Modifier.padding(16.dp)) {
                Text("نسخه", color=TXT, fontSize=15.sp)
                Text("SIMX v1.0.0 — AIOS Engine", color=SUB, fontSize=12.sp)
            }
        }
    }
}
""")

print("All Android project files generated successfully!")
