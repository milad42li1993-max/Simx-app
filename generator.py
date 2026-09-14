import os

def write(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

write("settings.gradle.kts", """
pluginManagement { repositories { google(); mavenCentral(); gradlePluginPortal() } }
dependencyResolutionManagement { repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS); repositories { google(); mavenCentral() } }
rootProject.name = "SIMX"
include(":app")
""")

write("build.gradle.kts", """
plugins { id("com.android.application") version "8.2.2" apply false; id("org.jetbrains.kotlin.android") version "1.9.22" apply false }
""")

write("gradle.properties", "org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8\nandroid.useAndroidX=true\nkotlin.code.style=official\n")

write("app/build.gradle.kts", """
plugins { id("com.android.application"); id("org.jetbrains.kotlin.android") }
android {
    namespace = "com.simx.app"
    compileSdk = 34
    defaultConfig { applicationId = "com.simx.app"; minSdk = 26; targetSdk = 34; versionCode = 3; versionName = "3.0.0" }
    buildTypes { release { isMinifyEnabled = false } }
    compileOptions { sourceCompatibility = JavaVersion.VERSION_17; targetCompatibility = JavaVersion.VERSION_17 }
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
    implementation("androidx.compose.material3:material3")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
}
""")

write("app/src/main/AndroidManifest.xml", """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <application android:allowBackup="true" android:label="SIMX" android:supportsRtl="true" android:theme="@style/Theme.SIMX">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter> <action android:name="android.intent.action.MAIN" /> <category android:name="android.intent.category.LAUNCHER" /> </intent-filter>
        </activity>
    </application>
</manifest>
""")

write("app/src/main/res/values/strings.xml", """<?xml version="1.0" encoding="utf-8"?><resources><string name="app_name">SIMX</string></resources>""")
write("app/src/main/res/values/themes.xml", """<?xml version="1.0" encoding="utf-8"?><resources><style name="Theme.SIMX" parent="android:Theme.Material.NoActionBar"><item name="android:statusBarColor">#0A0616</item><item name="android:windowBackground">#0A0616</item></style></resources>""")

# 8. MainActivity.kt (نسخه v3.0 Royal Purple + Simurgh + Market Tabs)
write("app/src/main/java/com/simx/app/MainActivity.kt", r"""
package com.simx.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.material3.TabRowDefaults.tabIndicatorOffset
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import kotlin.random.Random

// 🎨 پالت رنگی رویال بنفش و طلایی سیمرغ
val BgDark = Color(0xFF0A0616)       // بنفش بسیار تاریک (پس‌زمینه)
val CardDark = Color(0xFF17102A)     // بنفش تیره (کارت‌ها)
val AccentPurple = Color(0xFF9D4EDD) // بنفش نئونی (دکمه‌ها و اکتیوها)
val SimurghGold = Color(0xFFF3C623)  // طلایی لوکس سیمرغ
val BullGreen = Color(0xFF00E676)
val BearRed = Color(0xFFFF3D00)
val TextMain = Color(0xFFF8F9FA)
val TextSub = Color(0xFFA19CAD)
val Border = Color(0xFF2D234A)

data class LiveAsset(
    val category: String, // "crypto" or "forex"
    val symbol: String,
    val displayName: String,
    var price: Float,
    var change: Float,
    val bias: String,
    val narrative: String,
    val action: String,
    val chartPoints: MutableList<Float>
)

class MainActivity : ComponentActivity() {
    override fun onCreate(s: Bundle?) {
        super.onCreate(s)
        setContent { SimxV3App() }
    }
}

@Composable
fun SimxV3App() {
    var tab by remember { mutableIntStateOf(0) }
    var marketTab by remember { mutableIntStateOf(0) } // 0: Crypto, 1: Forex
    var selectedSymbolIndex by remember { mutableIntStateOf(0) }

    // لیست کامل دارایی‌ها با تفکیک بازار
    val allAssets = remember {
        mutableStateListOf(
            // --- Crypto ---
            LiveAsset("crypto", "BTC/USDT", "بیت‌کوین", 67450f, 3.4f, "صعودی", "جذب شدید سفارشات فروش در کف حمایتی. آماده شکست مقاومت ۶۹ هزار.", "خرید (LONG)", generateChart(true)),
            LiveAsset("crypto", "ETH/USDT", "اتریوم", 3520f, 2.1f, "صعودی", "رشد حجم معاملات در شبکه‌های لایه دو. روند صعودی همگام با بیت‌کوین.", "خرید (LONG)", generateChart(true)),
            LiveAsset("crypto", "SOL/USDT", "سولانا", 145f, 8.5f, "صعودی قدرتمند", "ورود سرمایه سنگین نهادی به شبکه سولانا. مقاومت بعدی ۱۵۵ دلار.", "خرید (LONG)", generateChart(true)),
            LiveAsset("crypto", "BNB/USDT", "بایننس‌کوین", 590f, -1.2f, "نزولی ضعیف", "فشار فروش ملایم در ناحیه مقاومتی. انتظار برای پولبک.", "صبر کنید", generateChart(false)),
            LiveAsset("crypto", "XRP/USDT", "ریپل", 0.62f, 0.5f, "خنثی", "نوسان رنج در فشردگی کامل. در انتظار اخبار دادگاه SEC.", "صبر کنید", generateChart(true)),
            LiveAsset("crypto", "ADA/USDT", "کاردانو", 0.45f, -2.4f, "نزولی", "خروج سرمایه و ضعف ساختار قیمت. احتمال ریزش تا ۰.۴۰.", "فروش (SHORT)", generateChart(false)),
            
            // --- Forex & Commodities ---
            LiveAsset("forex", "XAU/USD", "انس طلا", 2345.50f, 0.8f, "صبر و پایش", "فشردگی قیمت قبل از انتشار آمار تورم آمریکا. ریسک معاملات بالا است.", "صبر کنید", generateChart(true)),
            LiveAsset("forex", "EUR/USD", "یورو/دلار", 1.0825f, -0.4f, "نزولی", "تقویت شاخص دلار به دلیل لحن هاوکیش فدرال رزرو. یورو تحت فشار است.", "فروش (SHORT)", generateChart(false)),
            LiveAsset("forex", "GBP/USD", "پوند/دلار", 1.2640f, -0.2f, "رنج", "پوند در محدوده تصمیم‌گیری قرار دارد. عدم وجود جهت واضح.", "صبر کنید", generateChart(false)),
            LiveAsset("forex", "USD/JPY", "دلار/ین", 151.20f, 1.2f, "صعودی", "بانک مرکزی ژاپن تمایلی به مداخله ندارد. صعود دلار ادامه دارد.", "خرید (LONG)", generateChart(true))
        )
    }

    // شبیه‌ساز نوسان زنده و واقعی قیمت‌ها
    LaunchedEffect(Unit) {
        while (true) {
            delay(1500) // هر 1.5 ثانیه قیمت همه ارزها نوسان میکند
            for (i in allAssets.indices) {
                val asset = allAssets[i]
                val fluctuation = (Random.nextFloat() - 0.5f) * (asset.price * 0.001f) // نوسان 0.1 درصدی
                asset.price += fluctuation
                asset.chartPoints.removeAt(0)
                asset.chartPoints.add(asset.price)
                allAssets[i] = asset.copy() // تریگر برای آپدیت UI
            }
        }
    }

    val currentMarketAssets = allAssets.filter { if (marketTab == 0) it.category == "crypto" else it.category == "forex" }
    
    // جلوگیری از کرش هنگام تغییر تب بازار
    if (selectedSymbolIndex >= currentMarketAssets.size) selectedSymbolIndex = 0

    Column(Modifier.fillMaxSize().background(BgDark)) {
        // هدر با سیمرغ و بنفش رویال
        Row(
            Modifier.fillMaxWidth().padding(16.dp),
            Arrangement.SpaceBetween, Alignment.CenterVertically
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("🦅", fontSize = 28.sp) // نماد موقت سیمرغ
                Spacer(Modifier.width(8.dp))
                Text("SIMX", color = SimurghGold, fontSize = 24.sp, fontWeight = FontWeight.Black)
            }
            Surface(color = AccentPurple.copy(alpha = 0.15f), shape = RoundedCornerShape(12.dp)) {
                Row(Modifier.padding(horizontal = 10.dp, vertical = 6.dp), verticalAlignment = Alignment.CenterVertically) {
                    Box(Modifier.size(8.dp).clip(RoundedCornerShape(4.dp)).background(AccentPurple))
                    Spacer(Modifier.width(6.dp))
                    Text("AI Engine", color = AccentPurple, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                }
            }
        }

        // تب انتخاب بازار (کریپتو / فارکس)
        TabRow(
            selectedTabIndex = marketTab,
            containerColor = BgDark,
            contentColor = SimurghGold,
            indicator = { tabPositions ->
                Box(
                    Modifier.tabIndicatorOffset(tabPositions[marketTab])
                        .height(3.dp).padding(horizontal = 20.dp)
                        .clip(RoundedCornerShape(topStart = 3.dp, topEnd = 3.dp))
                        .background(AccentPurple)
                )
            },
            divider = { HorizontalDivider(color = Border) }
        ) {
            Tab(selected = marketTab == 0, onClick = { marketTab = 0; selectedSymbolIndex = 0 },
                text = { Text("کریپتوکارنسی", color = if (marketTab == 0) TextMain else TextSub, fontWeight = FontWeight.Bold) })
            Tab(selected = marketTab == 1, onClick = { marketTab = 1; selectedSymbolIndex = 0 },
                text = { Text("فارکس و طلا", color = if (marketTab == 1) TextMain else TextSub, fontWeight = FontWeight.Bold) })
        }

        // نوار انتخاب نماد
        LazyRow(
            Modifier.padding(vertical = 12.dp),
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(currentMarketAssets.size) { i ->
                val isSel = i == selectedSymbolIndex
                Text(
                    currentMarketAssets[i].symbol,
                    color = if (isSel) Color.White else TextSub,
                    fontSize = 13.sp, fontWeight = FontWeight.Bold,
                    modifier = Modifier.clip(RoundedCornerShape(20.dp))
                        .background(if (isSel) AccentPurple else CardDark)
                        .clickable { selectedSymbolIndex = i }
                        .padding(horizontal = 16.dp, vertical = 10.dp)
                )
            }
        }

        // محتوای اصلی
        Box(Modifier.weight(1f).padding(horizontal = 16.dp)) {
            if (currentMarketAssets.isNotEmpty()) {
                when (tab) {
                    0 -> DashboardView(currentMarketAssets[selectedSymbolIndex])
                    1 -> EventsView()
                    2 -> ChatView()
                    3 -> SettingsView()
                }
            }
        }

        // ناوبری پایین
        Row(
            Modifier.fillMaxWidth().background(CardDark).padding(vertical = 12.dp),
            Arrangement.SpaceEvenly
        ) {
            listOf("📊 تحلیل", "📅 اخبار", "🤖 دستیار", "⚙️ تنظیمات").forEachIndexed { i, l ->
                Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.clickable { tab = i }) {
                    Text(l, color = if (i == tab) AccentPurple else TextSub, fontSize = 12.sp, fontWeight = if (i == tab) FontWeight.Bold else FontWeight.Normal)
                }
            }
        }
    }
}

@Composable
fun DashboardView(asset: LiveAsset) {
    LazyColumn(verticalArrangement = Arrangement.spacedBy(14.dp)) {
        item {
            Card(colors = CardDefaults.cardColors(containerColor = CardDark), shape = RoundedCornerShape(20.dp)) {
                Column(Modifier.padding(20.dp)) {
                    Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween, Alignment.CenterVertically) {
                        Column {
                            Text(asset.displayName, color = TextMain, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                            Text(asset.symbol, color = TextSub, fontSize = 12.sp)
                        }
                        Column(horizontalAlignment = Alignment.End) {
                            val priceStr = if (asset.price > 10) String.format("$%,.2f", asset.price) else String.format("$%.4f", asset.price)
                            Text(priceStr, color = TextMain, fontSize = 24.sp, fontWeight = FontWeight.Black)
                            Text("${if (asset.change >= 0) "+" else ""}${asset.change}%", color = if (asset.change >= 0) BullGreen else BearRed, fontSize = 13.sp, fontWeight = FontWeight.Bold)
                        }
                    }

                    Spacer(Modifier.height(16.dp))

                    // نمودار گرافیکی با هاله رنگی
                    GradientSparkline(points = asset.chartPoints, isUp = asset.change >= 0)

                    Spacer(Modifier.height(20.dp))

                    val bColor = if (asset.bias.contains("صعودی")) BullGreen else if (asset.bias.contains("نزولی")) BearRed else SimurghGold
                    Surface(color = bColor.copy(alpha = 0.1f), shape = RoundedCornerShape(10.dp)) {
                        Text("🎯 سوگیری هوش مصنوعی: ${asset.bias}", color = bColor, fontSize = 14.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 14.dp, vertical = 8.dp))
                    }

                    Spacer(Modifier.height(16.dp))
                    Text("📖 تحلیل ساختار و جریان سفارشات:", color = AccentPurple, fontSize = 13.sp, fontWeight = FontWeight.Bold)
                    Spacer(Modifier.height(6.dp))
                    Text(asset.narrative, color = TextSub, fontSize = 14.sp, lineHeight = 22.sp)
                }
            }
        }

        if (asset.action != "صبر کنید") {
            item {
                Card(colors = CardDefaults.cardColors(containerColor = CardDark), shape = RoundedCornerShape(20.dp)) {
                    Column(Modifier.padding(20.dp)) {
                        val actColor = if (asset.action.contains("LONG") || asset.action.contains("خرید")) BullGreen else BearRed
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(Modifier.size(10.dp).clip(RoundedCornerShape(5.dp)).background(actColor))
                            Spacer(Modifier.width(8.dp))
                            Text("سیگنال: ${asset.action}", color = TextMain, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                        }
                        
                        Spacer(Modifier.height(16.dp))
                        Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween) {
                            Column { Text("محدوده ورود", color = TextSub, fontSize = 12.sp); Text(asset.entry, color = TextMain, fontSize = 14.sp, fontWeight = FontWeight.Bold) }
                            Column(horizontalAlignment = Alignment.End) { Text("حد ضرر", color = TextSub, fontSize = 12.sp); Text(asset.sl, color = BearRed, fontSize = 14.sp, fontWeight = FontWeight.Bold) }
                        }
                        Spacer(Modifier.height(12.dp))
                        Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween) {
                            Column { Text("هدف سود", color = TextSub, fontSize = 12.sp); Text(asset.tp, color = BullGreen, fontSize = 14.sp, fontWeight = FontWeight.Bold) }
                            Column(horizontalAlignment = Alignment.End) { Text("نسبت ریسک", color = TextSub, fontSize = 12.sp); Text(asset.rr, color = SimurghGold, fontSize = 14.sp, fontWeight = FontWeight.Bold) }
                        }

                        Spacer(Modifier.height(20.dp))
                        Button(
                            onClick = {}, Modifier.fillMaxWidth().height(50.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = AccentPurple),
                            shape = RoundedCornerShape(14.dp)
                        ) { Text("اجرای سیگنال", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 15.sp) }
                    }
                }
            }
        }
    }
}

@Composable
fun GradientSparkline(points: List<Float>, isUp: Boolean) {
    val lineColor = if (isUp) BullGreen else BearRed
    Canvas(modifier = Modifier.fillMaxWidth().height(60.dp)) {
        if (points.size < 2) return@Canvas
        val min = points.minOrNull() ?: 0f
        val max = points.maxOrNull() ?: 1f
        val range = if (max - min == 0f) 1f else max - min
        val w = size.width
        val h = size.height
        val step = w / (points.size - 1)

        val path = Path()
        val fillPath = Path()
        
        points.forEachIndexed { i, p ->
            val x = i * step
            val y = h - ((p - min) / range * h)
            if (i == 0) { path.moveTo(x, y); fillPath.moveTo(x, y) } 
            else { path.lineTo(x, y); fillPath.lineTo(x, y) }
        }
        
        fillPath.lineTo(w, h)
        fillPath.lineTo(0f, h)
        fillPath.close()

        drawPath(path = fillPath, brush = Brush.verticalGradient(listOf(lineColor.copy(alpha = 0.3f), Color.Transparent)))
        drawPath(path = path, color = lineColor, style = Stroke(width = 5f))
    }
}

// توابع کمکی برای تولید دیتای رندوم نمودار در نسخه تست
fun generateChart(isUp: Boolean): MutableList<Float> {
    val list = mutableListOf<Float>()
    var current = 100f
    for (i in 0..20) {
        current += if (isUp) Random.nextFloat() * 5f - 1f else Random.nextFloat() * 5f - 4f
        list.add(current)
    }
    return list
}

@Composable
fun EventsView() {
    Text("تقویم رویدادها در این نسخه آماده است...", color = TextMain)
}

@Composable
fun ChatView() {
    Text("دستیار هوشمند فعال است...", color = TextMain)
}

@Composable
fun SettingsView() {
    Text("تنظیمات سیستم...", color = TextMain)
}
""")

print("v3.0 Royal Purple with Simurgh Generated!")
