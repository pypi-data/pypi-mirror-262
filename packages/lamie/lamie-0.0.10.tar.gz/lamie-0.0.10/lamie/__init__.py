def p1():
    a = """
    program 1 : Basic operations JAVA CODE:

package com.example.arfanewapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.*;
import android.view.*;
public class ArithmeticOperation extends AppCompatActivity {
    EditText edtnum1,edtnum2,edtres;
    Button btnadd,btnsub,btnmul,btndiv;
    Double num1,num2,res;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_arithmetic_operation2);
        edtnum1=(EditText)findViewById(R.id.edtnum1);
        edtnum2=(EditText)findViewById(R.id.edtnum2);
        edtres=(EditText)findViewById(R.id.edtres);
        btnadd=(Button)findViewById(R.id.btnadd);
        btnsub=(Button)findViewById(R.id.btnsub);
        btnmul=(Button)findViewById(R.id.btnmul);
        btndiv=(Button)findViewById(R.id.btndiv);
    }
    public void Addition(View v)
    {
        num1=Double.parseDouble(edtnum1.getText().toString());
        num2=Double.parseDouble(edtnum2.getText().toString());
        res=num1+num2;
        edtres.setText(String.valueOf(res.toString()));
    }
    public void Subtraction(View v)
    {
        num1=Double.parseDouble(edtnum1.getText().toString());
        num2=Double.parseDouble(edtnum2.getText().toString());
        res=num1-num2;
        edtres.setText(String.valueOf(res.toString()));
    }
    public void Multiply(View v)
    {
        num1=Double.parseDouble(edtnum1.getText().toString());
        num2=Double.parseDouble(edtnum2.getText().toString());
        res=num1*num2;
        edtres.setText(String.valueOf(res.toString()));
    }
    public void Divide(View v)
    {
        num1=Double.parseDouble(edtnum1.getText().toString());
        num2=Double.parseDouble(edtnum2.getText().toString());
        res=num1/num2;
        edtres.setText(String.valueOf(res.toString()));
    }

}

XML CODE:

<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".ArithmeticOperation">
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/txthead"
        android:text="Arithmetic"
        android:textSize="20sp"
        android:textColor="@color/black"
        android:textAlignment="center"
        />
    <EditText
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/edtnum1"
        android:hint="Number 1"
        android:layout_below="@id/txthead"
        android:textColor="@color/black"
        android:textAlignment="center"
        />
    <EditText
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/edtnum2"
        android:hint="Number 2"
        android:layout_below="@id/edtnum1"
        android:textColor="@color/black"
        android:textAlignment="center"
        />
    <EditText
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/edtres"
        android:hint="Result"
        android:layout_below="@+id/edtnum2"
        android:textColor="@color/black"
        android:textAlignment="center"
        />
    <Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/btnadd"
        android:layout_below="@+id/edtres"
        android:onClick="Addition"
        android:text="+"
        />
    <Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/btnsub"
        android:layout_below="@+id/edtres"
        android:onClick="Subtraction"
        android:text="-"
        android:layout_toRightOf="@id/btnadd"
        />
    <Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/btnmul"
        android:layout_below="@+id/edtres"
        android:onClick="Multiply"
        android:text="*"
        android:layout_toRightOf="@id/btnsub"
        />
    <Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/btndiv"
        android:layout_below="@+id/edtres"
        android:onClick="Divide"
        android:text="/"
        android:layout_toRightOf="@id/btnmul"
        />

</RelativeLayout>
    """
    print(a)


def p2():
    b = """
    program 2 : Image view                                                                                                                                                                                                                 package com.example.arfanewapplication;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.*;
import android.view.*;



public class ImageOperationActivity extends AppCompatActivity {

    ImageView img1;
    RadioGroup rgopr;
    RadioButton rdopr;
    int i=1;
    int flag=0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_image_operation);
        img1=(ImageView) findViewById(R.id.img1);
        rgopr=(RadioGroup) findViewById(R.id.rgopr);

        rgopr.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup group, int checkedId) {
                rdopr=(RadioButton)findViewById(checkedId);

                if(rdopr.getText().toString().equals("Change Picture"))
                {
                    if(flag==0)
                    {
                        img1.setImageResource(R.drawable.img_1);
                        flag=1;
                    }
                    else
                    {
                        img1.setImageResource(R.drawable.img_2);
                        flag=0;
                    }
                }
                else if(rdopr.getText().toString().equals("Rotate Picture"))
                {
                    img1.setRotation(img1.getRotation()+90F);
                }
            }
        });
    }
}
XML CODE :

<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".ImageOperationActivity">



        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:id="@+id/txthead"
            android:text="Image Operations"
            android:textSize="24sp"
            android:textAlignment="center"
            />

        <ImageView
            android:layout_width="500px"
            android:layout_height="500px"
            android:id="@+id/img1"
            android:layout_centerHorizontal="true"
            android:src="@drawable/img_2"
            android:layout_below="@+id/txthead"
            />
        <RadioGroup
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:id="@+id/rgopr"
            android:layout_below="@+id/img1"
            android:orientation="horizontal"
            >
            <RadioButton
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:id="@+id/rdchange"
                android:text="Change Picture"
                />
            <RadioButton
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:id="@+id/rdrotate"
                android:text="Rotate Picture"
                />
        </RadioGroup>

    </RelativeLayout>
    """
    print(b)


def p3():
    c = """
    program 3 : notification                                                                                                                                                                                                                               package com.example.arfanewapplication;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.NotificationCompat;

import android.app.NotificationManager;
import android.view.*;
import android.widget.*;
import android.os.Bundle;

import java.util.ArrayList;

public class Notification extends AppCompatActivity {
    Button btnnotify;
    TextView txtid;
    EditText edtname,edtaddr;
    Spinner spcourse;
    ArrayList course = new ArrayList(10);
    ArrayAdapter adpt;
    int appno=100;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_notification);
        btnnotify=(Button)findViewById(R.id.btnnotify);
        txtid=(TextView)findViewById(R.id.txtid);
        edtname=(EditText)findViewById(R.id.edtname);
        edtaddr=(EditText)findViewById(R.id.edtaddr);
        spcourse=(Spinner)findViewById(R.id.spcourse);
        course.add("BCA");
        course.add("BSc");
        course.add("BCom");
        course.add("BA");
        adpt=new ArrayAdapter<>(getApplicationContext(), android.R.layout.simple_list_item_1,course);
        spcourse.setAdapter(adpt);
        txtid.setText(String.valueOf(appno));
    }
    public void Notify(View v)
    {
        NotificationCompat.Builder builder= new NotificationCompat.Builder(this);
        builder.setContentText("Application Number : "+appno+" Submitted");
        builder.setContentTitle("Application Form");
        builder.setSmallIcon(R.drawable.img);
        NotificationManager nm =(NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        Toast.makeText(getApplicationContext(),"Notification Recived",Toast.LENGTH_SHORT).show();
       nm.notify(0,builder.build());
        appno++;
        txtid.setText(String.valueOf(appno));

        edtname.setText("");
        edtaddr.setText("");

    }
}
XML CODE:

<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".Notification">

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/txthead"
        android:text="Application Form"
        android:textSize="24sp"
        android:textAlignment="center"
        />

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_below="@+id/txthead"
        android:id="@+id/txtid"
        />

    <EditText
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Name"
        android:layout_below="@+id/txtid"
        android:id="@+id/edtname"
        android:inputType="textPersonName"
        />

    <EditText
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Address"
        android:layout_below="@+id/edtname"
        android:id="@+id/edtaddr"
        android:inputType="textMultiLine"
        />

    <Spinner
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/spcourse"
        android:layout_below="@+id/edtaddr"
        />


    <Button
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/btnnotify"
        android:text="Notify"
        android:textSize="20sp"
        android:onClick="Notify"
        android:textAlignment="center"
        android:layout_below="@+id/spcourse"
        />

</RelativeLayout>
    """
    print(c)


def p4():
    d = """
    program 4 : linear layout                                                                                                                                                                                                                           package com.example.arfanewapplication;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.*;
import android.view.*;

public class Payroll extends AppCompatActivity {
    EditText edtbsal,edthra,edtda,edtgross,edtpf,edtnet;
    Double bsal,hra,da,pf,gross,net;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_payroll);

        edtbsal=(EditText)findViewById(R.id.edtbsal);
        edthra=(EditText)findViewById(R.id.edthra);
        edtda=(EditText)findViewById(R.id.edtda);
        edtpf=(EditText)findViewById(R.id.edtpf);
        edtgross=(EditText)findViewById(R.id.edtgross);
        edtnet=(EditText)findViewById(R.id.edtnet);
    }
    public void Calculate(View v)
    {
        bsal=Double.parseDouble(edtbsal.getText().toString());
        hra=0.1*bsal;
        da=0.12*bsal;
        pf=0.15*bsal;
        gross=bsal+da+hra;
        net=gross-pf;
        edthra.setText(String.valueOf("HRA : "+hra.toString()));
        edtda.setText(String.valueOf("DA : "+da.toString()));
        edtpf.setText(String.valueOf("PF : "+pf.toString()));
        edtgross.setText(String.valueOf("Gross Salary : "+gross.toString()));
        edtnet.setText(String.valueOf("Net Salary: "+net.toString()));

    }
}

XML CODE:

<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".Payroll">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/txthead"
        android:text="Payroll"
        android:textSize="24sp"
        android:layout_gravity="center"
        />
    <EditText
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/edtname"
        android:hint="Employee Name"

        android:textSize="20sp"
        />
    <EditText
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/edtbsal"
        android:hint="Basic Salary"
        android:textSize="20sp"
        />
    <EditText
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/edthra"
        android:hint="House Rent Allowance"
        android:textSize="20sp"
        android:onClick="Calculate"
        />
    <EditText
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/edtda"
        android:hint="Dearness Allowance"
        android:textSize="20sp"
        />
    <EditText
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/edtpf"
        android:hint="Provident Fund"
        android:textSize="20sp"
        />
    <EditText
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/edtgross"
        android:hint="Gross Salary"

        android:textSize="20sp"
        />
    <EditText
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/edtnet"
        android:hint="Net Salary"
        android:textSize="20sp"
        />
</LinearLayout>
    """
    print(d)


def p5():
    e = """
    prg 5 : login                                                                                                                                                                                                                                                           package com.example.arfanewapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle; import
        android.widget.*;
import android.view.*;

public class RelativelayoutActivity extends AppCompatActivity {

    EditText edtuname, edtpswd;
    Button btnlogin,btnrefresh;

    @Override
    protected void onCreate(Bundle SavedInstanceState) {
        super.onCreate(SavedInstanceState);
        setContentView(R.layout.activity_relativelayout);
        edtuname=(EditText) findViewById(R.id.edtuname);
        edtpswd=(EditText) findViewById(R.id.edtpswd);
        btnlogin=(Button) findViewById(R.id.btnlogin);
        btnrefresh=(Button) findViewById(R.id.btnrefresh);
    }
    public void Login(View v)
    {
        if(edtuname.getText().toString().equals("arfa") &&
                edtpswd.getText().toString().equals("arfa123"))
        {
            Intent in=new Intent(this,ProuductActivity.class);
            startActivity(in);
        }
        else
        {
            Toast.makeText(getApplicationContext(),"Invalid user",Toast.LENGTH_SHORT).show();
        }
    }
    public void Refresh(View v)
    {
        edtuname.setText("");
        edtpswd.setText("");
    }
}

XML CODE:

<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".RelativelayoutActivity">

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/txthead"
        android:layout_marginTop="20dp"
        android:text="LOGIN"
        android:textSize="24sp"
        android:textAlignment="center"
        />
    <ImageView
        android:layout_width="200px"
        android:layout_height="200px"
        android:id="@+id/imglogin"
        android:src="@drawable/img"
        android:layout_centerHorizontal="true"
        android:layout_below="@+id/txthead"
        />
    <EditText
        android:layout_width="150dp"
        android:layout_height="wrap_content"
        android:id="@+id/edtuname"
        android:hint="Username"
        android:textAlignment="center"
        android:layout_centerHorizontal="true"
        android:textSize="20sp"
        android:layout_below="@+id/imglogin"
        />
    <EditText
        android:layout_width="150dp"
        android:layout_height="wrap_content"
        android:id="@+id/edtpswd"
        android:hint="Password"
        android:textAlignment="center"
        android:layout_centerHorizontal="true"
        android:textSize="20sp"
        android:layout_below="@+id/edtuname"

        android:inputType="textPassword"
        />
    <Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/btnlogin"
        android:text="Login"
        android:layout_below="@+id/edtpswd"
        android:onClick="Login"
        android:layout_centerHorizontal="true"
        />
    <Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/btnrefresh"
        android:text="Refresh"
        android:layout_below="@+id/edtpswd"
        android:layout_toRightOf="@+id/btnlogin"
        android:onClick="Refresh"
        android:layout_centerHorizontal="true"
        />
    </RelativeLayout>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       product details :                                                                                                                                                                                                                                                       package com.example.arfanewapplication;

import androidx.appcompat.app.AppCompatActivity;
import android.widget.*;
import android.view.*;
import android.os.Bundle;
public class ProuductActivity extends AppCompatActivity {

    ImageView imgiphone,imgredmi,imgsamsung;
    TextView txtiphone,txtsamsung,txtredmi;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_prouduct);

        imgiphone=(ImageView) findViewById(R.id.imgiphone);
        imgredmi=(ImageView) findViewById(R.id.imgredmi);
        imgsamsung=(ImageView) findViewById(R.id.imgsamsung);
        txtiphone=(TextView) findViewById(R.id.txtiphone);
        txtredmi=(TextView) findViewById(R.id.txtredmi);
        txtsamsung=(TextView)findViewById(R.id.txtsamsung);
    }
    public void IphoneDisplay(View v)
    {
        txtiphone.setText("Model : Apple iPhone 13 (128GB) \n Color : Pink \n Price : ₹52,999 ");
    }
    public void RedmiDisplay(View v)
    {
        txtredmi.setText("Model : Redmi 12 5G \n Color : Jade Black \n Price : ₹13,499 ");
    }
    public void SamsungDisplay(View v)
    {
        txtsamsung.setText("Model : Samsung Galaxy M04 \n Color : Light Green \n Price : ₹8,028 ");
    }
    }




XML CODE:

<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".ProuductActivity">


        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:id="@+id/txthead"
            android:text="ProductDetails"
            android:textSize="24sp"
            android:textAlignment="center"/>
        <ImageView
            android:layout_width="500px"
            android:layout_height="500px"
            android:id="@+id/imgiphone"
            android:onClick="IphoneDisplay"
            android:src="@drawable/img_1"
            android:layout_below="@+id/txthead"/>
        <TextView
    android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:id="@+id/txtiphone"
            android:textSize="24sp"
            android:textAlignment="center"
            android:layout_below="@+id/txthead"
            android:layout_toRightOf="@+id/imgiphone"/>
        <ImageView
            android:layout_width="500px"
            android:layout_height="500px"
            android:id="@+id/imgredmi"
            android:onClick="RedmiDisplay"
            android:src="@drawable/img_2"
            android:layout_below="@+id/imgiphone"/>
        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:id="@+id/txtredmi"
            android:textSize="24sp"
            android:textAlignment="center"
            android:layout_below="@+id/imgiphone"
            android:layout_toRightOf="@+id/imgredmi"/>
        <ImageView
            android:layout_width="500px"
            android:layout_height="500px"
            android:id="@+id/imgsamsung"
            android:onClick="SamsungDisplay"
            android:src="@drawable/img_3"
            android:layout_below="@+id/imgredmi"/>
        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:id="@+id/txtsamsung"
            android:textSize="24sp"
            android:textAlignment="center"
            android:layout_below="@+id/imgredmi"
            android:layout_toRightOf="@+id/imgsamsung"/>


    </RelativeLayout>
    """
    print(e)


def p6():
    f = """
    program 6 : table layout                                                                                                                                                                                                                             package com.example.arfanewapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

public class Tablelayout extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_tablelayout);
    }
}

XML CODE:

<?xml version="1.0" encoding="utf-8"?>
<TableLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".Tablelayout">

    <TableRow
        android:layout_height="wrap_content"
        android:layout_width="match_parent"
        >

        <TextView
            android:layout_height="wrap_content"
            android:layout_width="match_parent"
            android:id="@+id/txthead"
            android:text="Product Details"
            android:textSize="24sp"
            android:layout_gravity="center"
            android:layout_span="2"

            />

    </TableRow>
    <TableRow>
        <ImageView
            android:layout_width="500px"
            android:layout_height="500px"
            android:id="@+id/imgiphone"
            android:src="@drawable/img_1"
            android:scaleType="fitCenter"
            />
        <ImageView
            android:layout_width="500px"
            android:layout_height="500px"
            android:id="@+id/imgsamsung"
            android:src="@drawable/img_2"
            android:scaleType="fitCenter"
            />

    </TableRow>
    <TableRow
        android:background="@color/design_default_color_secondary_variant">
        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:id="@+id/txtdet1"
            android:text="Apple iPhone 13 "
            android:textSize="20sp"
            android:layout_gravity="center"

            />
        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:id="@+id/txtdet2"
            android:text="Samsung Galaxy M04 "
            android:textSize="20sp"
            android:layout_gravity="center"
            />
    </TableRow>
    <TableRow>
        <ImageView
            android:layout_width="500px"
            android:layout_height="500px"
            android:id="@+id/imgiphone2"
            android:src="@drawable/img_3"
            android:scaleType="fitCenter"
            />
        <ImageView
            android:layout_width="500px"
            android:layout_height="500px"
            android:id="@+id/imgsamsung2"
            android:src="@drawable/img"
            android:scaleType="fitCenter"
            />

    </TableRow>
    <TableRow
        android:background="@color/design_default_color_secondary_variant">
        >
        <TextView
            android:layout_width="wrap_content"

            android:layout_height="wrap_content"
            android:id="@+id/txtdet3"
            android:text="Apple iPhone 13 "
            android:textSize="20sp"
            android:layout_gravity="center"
            />
        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:id="@+id/txtdet4"
            android:text="Samsung Galaxy M04 "
            android:textSize="20sp"
            android:layout_gravity="center"
            />
    </TableRow>
</TableLayout>  
    """
    print(f)


def p7():
    g = """
    program 7 : input methods                                                                                                                                                                                                                  package com.example.bcaapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.inputmethod.EditorInfo;
import android.widget.*;
import android.view.*;

public class MainActivity extends AppCompatActivity {
EditText edtname,edtaddr,edtphno,edtemail;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        edtname=(EditText) findViewById(R.id.edtname);
        edtaddr=(EditText) findViewById(R.id.edtaddr);
        edtphno=(EditText) findViewById(R.id.edtphno);
        edtemail=(EditText) findViewById(R.id.edtemail);
        edtemail.setOnEditorActionListener(new TextView.OnEditorActionListener() {
            @Override
            public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
                if(actionId== EditorInfo.IME_ACTION_DONE)
                {
                    if(edtname.getText().toString().isEmpty() edtaddr.getText().toString().isEmpty()||edtphno.getText().toString().isEmpty()||edtemail.getText().toString().isEmpty())
                    {
                        Toast.makeText(MainActivity.this, "All input fields are mandatory", Toast.LENGTH_SHORT).show();
                    }
                    else if (edtphno.getText().toString().length()!=10)
                    {
                        Toast.makeText(MainActivity.this, "Enter a valid mobile number", Toast.LENGTH_SHORT).show();
                    }
                    else if ((edtemail.getText().toString().indexOf('@')==-1)  (edtemail.getText().toString().indexOf('.')==-1))

                    {
                        Toast.makeText(MainActivity.this, "Enter a valid Mail ID", Toast.LENGTH_SHORT).show();
                    }
                    else
                    {
                        Toast.makeText(MainActivity.this, "Validated Successfully", Toast.LENGTH_SHORT).show();
                    }

                }
                return false;
            }
        });
    }
}

Xml
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/txthead"
        android:text="Registration"
        android:textSize="25sp"
        android:textAlignment="center"></TextView>
    <EditText
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/edtname"
        android:hint="Name"
        android:digits="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        android:inputType="textPersonName"
        android:layout_below="@+id/txthead"></EditText>

    <EditText
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/edtaddr"
        android:hint="Address"
        android:inputType="textMultiLine"
        android:layout_below="@+id/edtname"></EditText>
    <EditText
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/edtphno"
        android:hint="Mobile Number"
        android:inputType="phone"
        android:layout_below="@+id/edtaddr"></EditText>
    <EditText
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/edtemail"
        android:hint="Email ID"
        android:inputType="textEmailAddress"
        android:layout_below="@+id/edtphno"
        android:imeOptions="actionDone">
    </EditText>

</RelativeLayout>
        """
    print(g)



def p8():
    h = """
    program 8 : audio                                                                                                                                                                                                                                     package com.example.arfanewapplication;

import androidx.appcompat.app.AppCompatActivity;
import android.media.MediaPlayer;
import android.widget.*;
import android.view.*;
import android.os.Bundle;

public class AudioActivity extends AppCompatActivity {
    Button btnplay,btnpause,btnstop;
    MediaPlayer mp;

    int pos;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_audio);

        btnplay=(Button) findViewById(R.id.btnplay);
        btnpause=(Button) findViewById(R.id.btnpause);
        btnstop=(Button) findViewById(R.id.btnstop);

    }
    public void PlaySong(View v)
    {
        mp=MediaPlayer.create(this,R.raw.audio);
        mp.start();
        Toast.makeText(getApplicationContext(),"Song is playing",Toast.LENGTH_SHORT).show();


    }
    public void PauseSong(View v)
    {
        if(mp.isPlaying())
        {
            pos=mp.getCurrentPosition();
            mp.pause();
            Toast.makeText(getApplicationContext(),"Song is pause",Toast.LENGTH_SHORT).show();

        }
        else
        {
            mp.seekTo(pos);
            mp.start();
        }
    }

    public void StopSong(View v)
    {
        if(mp.isPlaying())
        {
            mp.stop();
            Toast.makeText(getApplicationContext(),"Song has stopped",Toast.LENGTH_SHORT).show();

        }
    }

}


XML CODE :

<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".AudioActivity">

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/txthead"
        android:text="Spotify"
        android:textAlignment="center"
        android:textSize="24sp"
        />

    <ImageView
        android:layout_width="200px"
        android:layout_height="200px"
        android:src="@drawable/wynk"
        android:id="@+id/imgicon"
        android:layout_below="@+id/txthead"
        android:layout_centerHorizontal="true"
        />

    <Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/btnplay"
        android:text="Play"
        android:layout_below="@+id/imgicon"
        android:onClick="PlaySong"
        />

    <Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/btnpause"
        android:text="Pause"
        android:layout_below="@+id/imgicon"
        android:layout_toRightOf="@+id/btnplay"
        android:onClick="PauseSong"
        />

    <Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/btnstop"
        android:text="Stop"
        android:layout_below="@+id/imgicon"
        android:layout_toRightOf="@+id/btnpause"
        android:onClick="StopSong"
        />



</RelativeLayout>
                """
    print(h)



def p9():
    i = """
    program 9 : read and write                                                                                                                                                                                                                  import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class ShareActivity extends AppCompatActivity {
    EditText edtid, edtn, edtsal, edtde;
    Button btnwrite, btnread;
    SharedPreferences pref;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_share);
        edtn = (EditText) findViewById(R.id.edtn);
        edtde = (EditText) findViewById(R.id.edtde);
        edtsal = (EditText) findViewById(R.id.edtsal);
        btnread = (Button) findViewById(R.id.btnread);
        btnwrite = (Button) findViewById(R.id.btnwrite);
        SharedPreferences pref =getSharedPreferences("MyFile",MODE_PRIVATE);
    }
    public void WriteData(View v)
    {
        SharedPreferences.Editor edit= pref.edit();
        edit.putString("EmpID",edtid.getText().toString());
        edit.putString("EmpName",edtn.getText().toString());
        edit.putString("EmpDepartment",edtde.getText().toString());
        edit.putString("EmpSalary",edtsal.getText().toString());
        edit.commit();
        Toast.makeText(this, "Data Written Successfully", Toast.LENGTH_LONG).show();
        edtid.setText("");
        edtn.setText("");
        edtde.setText("");
        edtsal.setText("");
    }
    public void ReadData(View v)
    {
        if(pref.contains("EmpID")){
            edtid.setText(pref.getString("EmpID",null));
            edtn.setText(pref.getString("EmpName",null));
            edtde.setText(pref.getString("EmpDepartment",null));
            edtsal.setText(pref.getString("EmpSalary",null));
        }
    }
}
xml code:
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".ShareActivity">
    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/txthead"
        android:text="Employee details"
        android:textSize="25sp"
        android:textAlignment="center">
    </TextView>
    <EditText
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/edtid"
        android:textSize="25sp"
        android:hint="Employee ID"
        android:textAlignment="center"
        android:layout_below="@+id/txthead">
    </EditText>
    <EditText
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/edtn"
        android:hint="Employee Name"
        android:textSize="25sp"
        android:textAlignment="center"
        android:layout_below="@+id/edtid">
    </EditText>
    <EditText
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/edtde"
        android:hint="Employee Department"
        android:textSize="25sp"
        android:textAlignment="center"
        android:layout_below="@+id/edtn">
    </EditText>
    <EditText
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/edtsal"
        android:hint="Employee Salary"
        android:textSize="25sp"
        android:textAlignment="center"
        android:layout_below="@+id/edtde">
    </EditText>
    <Button
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/btnwrite"
        android:layout_below="@+id/edtsal"
        android:text="Read Data"
        android:onClick="ReadData">
    </Button>
    <Button
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/btnread"
        android:layout_below="@+id/btnwrite"
        android:text="Write Data"
        android:onClick="WriteData">
    </Button>


</RelativeLayout>

        """
    print(i)


def p10():
    j = """
    program 10 : list view                                                                                                                                                                                                                               package com.example.arfanewapplication;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.*;
import android.view.*;
import java.util.ArrayList;
public class Listview extends AppCompatActivity {

    ListView lstbook,lstbookselected;
    ArrayList book=new ArrayList(10);
    ArrayList bookselected=new ArrayList(10);
    ArrayAdapter adpt,adpt1;
    Button btnclear;

    @Override

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_listview);

        lstbook=(ListView)findViewById(R.id.lstbook);
        lstbookselected=(ListView) findViewById(R.id.lstbookselected);
        btnclear=(Button) findViewById(R.id.btnclear);
        book.add("C Programming");
        book.add("C# Programming");
        book.add("JavaScript");
        book.add("Java");
        book.add("Python");
        book.add("Pascal");
        book.add("JSON");
        book.add("CSS");
        adpt=new ArrayAdapter(getApplicationContext(),
                android.R.layout.simple_list_item_single_choice,book);
        lstbook.setAdapter(adpt);
        lstbook.setChoiceMode(AbsListView.CHOICE_MODE_SINGLE);
        lstbook.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                if(bookselected.contains(lstbook.getItemAtPosition(position)))
                {
                    Toast.makeText(getApplicationContext(),"Item ALready Selected",Toast.LENGTH_SHORT).show();
                }
                else {
                    bookselected.add(lstbook.getItemAtPosition(position));

                    adpt1=new ArrayAdapter(getApplicationContext(),
                            android.R.layout.simple_list_item_single_choice,bookselected);
                    lstbookselected.setAdapter(adpt1);
                }

            }
        });
        lstbookselected.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Toast.makeText(getApplicationContext(),lstbookselected.getItemAtPosition(position)+" Removed",Toast.LENGTH_SHORT).show();
                        bookselected.remove(position);
                adpt1.notifyDataSetChanged();
            }
        });

    }
    public void ClearItems(View v)
    {
        bookselected.clear();
        adpt1.notifyDataSetChanged();
        Toast.makeText(getApplicationContext(),"All Items Are Cleared",Toast.LENGTH_SHORT).show();

    }

}

XML CODE:
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".Listview">

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
    android:id="@+id/txthead"
        android:layout_marginTop="20dp"
        android:text="Book Details"
        android:textSize="24sp"
        android:textAlignment="center"
        android:textStyle="bold"
        />
    <ListView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/lstbook"
        android:layout_below="@+id/txthead"
        />
    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/txtselected"
        android:layout_marginTop="20dp"
        android:text="Books Selected"
        android:textSize="24sp"
        android:textAlignment="center"
        android:textStyle="bold"
        android:layout_below="@+id/lstbook"
        />
    <ListView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/lstbookselected"
        android:layout_below="@+id/txtselected"
        />
    <Button
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/btnclear"
        android:text="Clear"
        android:layout_below="@+id/lstbookselected"
        android:layout_centerHorizontal="true"
        android:onClick="ClearItems"
        />
</RelativeLayout>

        """
    print(j)


def p11():
    k = """
    program 11 : spinner view                                                                                                                                                                                                                      package com.example.arfanewapplication;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.*;
import android.view.*;
import java.util.ArrayList;


public class Spinneractivity extends AppCompatActivity {
    Spinner spmenu;
    ListView lstmenu;
    Button btnadd;
    EditText edtprice, edtamt, edtqty, edttotal;
    ArrayList menu = new ArrayList<>(20);
    ArrayList selected = new ArrayList<>(20);
    ArrayAdapter adpt, adpt1;
    Double amt,total=0.0,qty,price;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_spinneractivity);
        spmenu = (Spinner)findViewById(R.id.spmenu);
        lstmenu = (ListView) findViewById(R.id.lstmenu);
        btnadd = (Button) findViewById(R.id.btnadd);
        edtprice = (EditText) findViewById(R.id.edtprice);
        edtqty = (EditText) findViewById(R.id.edtqty);
        edtamt = (EditText) findViewById(R.id.edtamt);
        edttotal = (EditText) findViewById(R.id.edttotal);
        menu.add("Pizza");
        menu.add("Pasta");
        menu.add("Burger");
        menu.add("Cake");
        menu.add("Peri Peri Fries");
        adpt = new ArrayAdapter<>(getApplicationContext(), android.R.layout.simple_list_item_1,
                menu);
        spmenu.setAdapter(adpt);
        lstmenu.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override

            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                edtamt.setText("");
                edtqty.setText("");
                if(lstmenu.getItemAtPosition(position)=="Pizza")
                {
                    edtprice.setText(String.valueOf(300));
                }
                else if (lstmenu.getItemAtPosition(position)=="Pasta")
                {
                    edtprice.setText(String.valueOf(280));
                }
                else if (lstmenu.getItemAtPosition(position)=="Burger")
                {
                    edtprice.setText(String.valueOf(180));
                }
                else if (lstmenu.getItemAtPosition(position)=="Cake")
                {
                    edtprice.setText(String.valueOf(550));
                }
                else if (lstmenu.getItemAtPosition(position)=="Peri Peri Fries")
                {
                    edtprice.setText(String.valueOf(80));
                }
            }
        });
    }
    public void AddItem(View v) {
        if (selected.contains(spmenu.getSelectedItem())) {
            Toast.makeText(getApplicationContext(), "Item ALready Selected",
                    Toast.LENGTH_SHORT).show();
        } else {
            selected.add(spmenu.getSelectedItem());
            adpt1 = new ArrayAdapter<>(getApplicationContext(),
                    android.R.layout.simple_list_item_multiple_choice, selected);
            lstmenu.setAdapter(adpt1);
            lstmenu.setChoiceMode(AbsListView.CHOICE_MODE_MULTIPLE);
        }
    }
    public void Display(View v)
    {
        price=Double.parseDouble(edtprice.getText().toString());
        qty=Double.parseDouble(edtqty.getText().toString());
        amt=price*qty;
        total=total+amt;
        edtamt.setText(String.valueOf(amt));

        edttotal.setText(String.valueOf(total));
    }
}

XML CODE:

<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".Spinneractivity">

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/txthead"
        android:text="MENU"
        android:textSize="24sp"
        android:textAlignment="center"
        />
    <Spinner
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/spmenu"
        android:layout_below="@+id/txthead"
        />
    <Button
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/btnadd"
        android:text="add"
        android:layout_below="@+id/spmenu"
        android:onClick="AddItem"
        />
    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/txtmenuselected"
        android:text="Selected Items"
        android:textSize="24sp"
        android:textAlignment="center"

        android:layout_below="@+id/btnadd"
        />
    <ListView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/lstmenu"
        android:layout_below="@+id/txtmenuselected"
        />
    <EditText
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/edtprice"
        android:layout_below="@+id/lstmenu"
        android:hint="Price"
        />
    <EditText
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/edtqty"
        android:layout_below="@+id/lstmenu"
        android:layout_toRightOf="@+id/edtprice"
        android:hint="Quantity"
        />
    <EditText
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/edtamt"
        android:layout_below="@+id/lstmenu"
        android:layout_toRightOf="@+id/edtqty"
        android:hint="Amount"
        android:onClick="Display"
        />
    <EditText
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/edttotal"
        android:layout_below="@+id/lstmenu"
        android:layout_toRightOf="@+id/edtamt"
        android:hint="Grand Total"
        />

</RelativeLayout>

        """
    print(k)


def p12():
    l = """
    program 12 : sub menu                                                                                                                                                                                                                      package com.example.arfanewapplication;

import androidx.appcompat.app.AppCompatActivity;


import android.widget.*;
import android.view.*;
import android.os.Bundle;

public class PopUpActivity extends AppCompatActivity {
    Button btndisplay;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pop_up);
        btndisplay = (Button) findViewById(R.id.btndisplay);

    }
    public void DisplayMenu(View v)
    {
        PopupMenu pop= new PopupMenu(this,v);
        MenuInflater inf= pop.getMenuInflater();
        inf.inflate(R.menu.menu,pop.getMenu());
        pop.show();
        pop.setOnMenuItemClickListener(new PopupMenu.OnMenuItemClickListener() {
            @Override
            public boolean onMenuItemClick(MenuItem item) {
                if(item.getTitle().equals("Play"))
                {
                    Toast.makeText(getApplicationContext(),"Play has been selected",Toast.LENGTH_SHORT).show();
                }
                else if (item.getTitle().equals("Pause"))
                {
                    Toast.makeText(getApplicationContext(),"Pause has been selected",Toast.LENGTH_SHORT).show();
                }
                else if (item.getTitle().equals("Stop"))
                {
                    Toast.makeText(getApplicationContext(),"Stop has been selected",Toast.LENGTH_SHORT).show();
                }
                return true;
            }
        });
    }

}

XML CODE:

<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".PopUpActivity">

    <Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/btndisplay"
        android:text="Display"
        android:onClick="DisplayMenu"/>
</RelativeLayout>

        """
    print(l)



def p13():
    m = """
    program 13 : context menu                                                                                                                                                                                                                  package com.example.arfanewapplication;

import androidx.appcompat.app.AppCompatActivity;


import android.widget.*;
import android.view.*;
import android.os.Bundle;
public class MenuContextActivity extends AppCompatActivity {
    Button btndisplay;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu_context);

        btndisplay=(Button)findViewById(R.id.btndisplay);
        registerForContextMenu(btndisplay);
    }
    public void onCreateContextMenu(ContextMenu m, View v, ContextMenu.ContextMenuInfo info)
    {
        MenuInflater inf= getMenuInflater();
        inf.inflate(R.menu.contextmenu,m);
    }
    public boolean onContextItemSelected (MenuItem item)
    {
        if(item.getTitle().equals("Play"))
        {
            Toast.makeText(getApplicationContext(),"Play has been selected",Toast.LENGTH_SHORT).show();

        }
        else if (item.getTitle().equals("Pause"))
        {
            Toast.makeText(getApplicationContext(),"Pause has been selected",Toast.LENGTH_SHORT).show();
        }
        else if (item.getTitle().equals("Stop"))
        {
            Toast.makeText(getApplicationContext(),"Stop has been selected",Toast.LENGTH_SHORT).show();
        }

        return  true;
    }

}
XML CODE:

<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MenuContextActivity">


    <Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/btndisplay"
        android:text="Display Menu"
        />
</RelativeLayout>
OUTPUT:
(LONG PRESS ON DISPLAY MENU IT WILL GIVE THE OUTPUT)

        """
    print(m)


def p14():
    n = """
    program 14 : location and map                                                                                                                                                                                                             package com.example.sakeenaapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.*;
import android.widget.*;

public class TrackLocationActivity extends AppCompatActivity {
    EditText edtloc;
    Button btndisplay;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_track_location);
        edtloc=(EditText) findViewById(R.id.edtloc);
        btndisplay=(Button) findViewById(R.id.btndisplay);
    }

    public void DisplayLocation(View v)
    {

    }
}                                                                                                                                                                                                                                                                     xml code :                                                                                                                                                                                                                                                      <?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".TrackLocationActivity">

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/txthead"
        android:text="TRACK LOCATION"
        android:layout_marginTop="30dp"
        android:textSize="30sp"
        android:textAlignment="center"
        android:textStyle="bold"
        />

    <EditText
        android:layout_marginTop="20dp"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint=""
        android:id="@+id/edtloc"
        android:textAlignment="center"
        android:layout_below="@+id/txthead"
        />

    <Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:id="@+id/btndisplay"
        android:text="Display Location"
        android:layout_marginTop="30dp"
        android:layout_centerHorizontal="true"
        android:layout_below="@+id/edtloc"
        android:onClick="DisplayLocation"
        />


</RelativeLayout>

        """
    print(n)


def p15():
    o = """
    program 15 : database activity                                                                                                                                                                                                                     package com.example.myapplication;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.os.Bundle;

import java.util.ArrayList;

public class DatabaseActivity extends SQLiteOpenHelper {
    public static final String db = "Student";
    public static final String tb = "stud";
    public static final String col1="regno";
    public static final String col2="name";
    String query;
    ArrayList details = new ArrayList(10);

    public DatabaseActivity(@Nullable Context context ) {
        super(context, db, null , 1);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        query= "create table " +tb+"( "+col1+" text, "+col2+" text )";
        db.execSQL(query);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {

    }

    public void InsertStud(String regno, String name)
    {
        SQLiteDatabase db = getWritableDatabase();
        ContentValues cv = new ContentValues();
        cv.put(col1,regno);
        cv.put(col2,name);
        db.insert(tb,null,cv);
    }

    public ArrayList DisplayStudent()
    {
        SQLiteDatabase db = getReadableDatabase();
        Cursor cu = db.rawQuery("select * from "+tb,null);
        while(cu.moveToNext())
        {
            details.add(cu.getString(0 )+ "\t \t"+cu.getString(1));
        }
        return details;
    }
}                                                                                                                                                                                                                                                                          xml code:                                                                                                                                                                                                                                                                  <?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".DatabaseActivity">

</androidx.constraintlayout.widget.ConstraintLayout>                                                                                                                                                                                    Database Insert :                                                                                                                                                                                                                                                 package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;
import android.widget.*;
import android.view.*;
import android.os.Bundle;

import java.util.ArrayList;

public class DatabaseInsertActivity extends AppCompatActivity {
    EditText edtname, edtregno;
    Button btninsert, btndisplay;
    ListView lststudent;
    ArrayList stud = new ArrayList(10);
    ArrayAdapter adpt;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_database_insert);

edtregno= (EditText) findViewById(R.id.edtregno);
        edtname= (EditText) findViewById(R.id.edtname);
        btninsert=(Button)findViewById(R.id.btninsert);
        btndisplay=(Button)findViewById(R.id.btndisplay);
        lststudent = (ListView) findViewById(R.id.lststudent);

    }

    public void InsertStudent(View v)
    {
        DatabaseActivity dba = new DatabaseActivity(this);
        dba.InsertStud(edtregno.getText().toString(),edtname.getText().toString());
        Toast.makeText(getApplicationContext(), "Record inserted sucessfully",Toast.LENGTH_LONG).show();
        edtregno.setText("");
        edtname.setText("");
    }
    public void DisplayStudent(View v )
    {

        DatabaseActivity dba = new DatabaseActivity(this);
        stud=dba.DisplayStudent();
        adpt= new ArrayAdapter(getApplicationContext(), android.R.layout.simple_list_item_1,stud);
        lststudent.setAdapter(adpt);
    }
}                                                                                                                                                                                                                                                                              xml code:                                                                                                                                                                                                                                                          <?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".DatabaseInsertActivity">

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/txthead"
        android:text="Student Details"
        android:textSize="24sp"
        android:textAlignment="center"/>

    <EditText
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/edtregno"
        android:hint="Register Number"
        android:layout_below="@+id/txthead"
        />

    <EditText
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/edtname"
        android:hint="Name"
        android:layout_below="@+id/edtregno"
        />

    <Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Insert"
        android:id="@+id/btninsert"
        android:layout_below="@id/edtname"
        android:onClick="InsertStudent"
        />

    <Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Display"
        android:id="@+id/btndisplay"
        android:layout_below="@id/edtname"
        android:layout_toRightOf="@+id/btninsert"
        android:onClick="DisplayStudent"
        />

    <ListView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:id="@+id/lststudent"
        android:layout_below="@+id/btndisplay"
        />



</RelativeLayout>
        """
    print(o)	
