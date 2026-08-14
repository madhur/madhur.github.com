---
slug: "silverlight-people-picker"
title: >-
  Writing Silverlight people picker control using SharePoint 2010 Client object
  model
date: '2014-01-29'
description: >-
  Writing Silverlight people picker control using SharePoint 2010 Client object
  model
tags:
  - Silverlight
  - SharePoint 2010
draft: false
categories:
  - Web Development
params:
  disqus_id: /2014/01/29/silverlight-people-picker/
  location: 'New Delhi, India'
  time: '9:00 PM'
---

Whenever you are developing a silverlight solution on SharePoint 2010, one of the basic functionality you will require is the ability to select people from your Active Directory.

Sadly, I could not find a ready made custom silverlight control which I could utilize for my solution. I decided to write on my own. Rather than writing from scratch, I decided to
use the boilerplate code [provided](http://blogs.technet.com/b/speschka/archive/2011/08/09/writing-a-sharepoint-2010-people-picker-control-for-silverlight.aspx) by Steve.

In this post, I am going to deep dive how I built this control.

My solution consists of two controls, `PeopleChooser` and `PeoplePicker`. `PeopleChooser` is a user control which is configured to either single select or multi select depending upon the 
configuration.  Here’s a screenshot of my people Chooser control, implemented as a user control in Silverlight.

![PeopleChooser Single Selection](/images/Blog/singlepicker.png)

In case of multiple results, user can right click on the textbox to display multiple results and select one of them.

![PeopleChooser Multiple results](/images/Blog/pickermultipleresults.png)

The multi select configuraiton is rendered as a listbox instead of a textbox. I made a conscious design decision to do this so that user instantly comes to know that this is a multi select
picker by directly looking at it. 

![PeopleChooser Multiple selection](/images/Blog/multiplepicker.png)

`PeoplePicker` is a `ChildWindow` which is launched from the `PeopleChooser` to search and enumerate people from the active directory. 
Clicking on the address book button opens the people picker, where the user can select either multiple people or single people depending upon the configuration of the control.
This is the screenshot of  people picker control. 

![PeoplePicker](/images/Blog/peoplepicker.png)

Feel free to [download](https://github.com/madhur/SLControls/archive/master.zip) this control or customize by downloding the source from my [github repo](https://github.com/madhur/SLControls)

Anyone, who wants to reuse or customize this control further, I will explain in brief how this works. 

Both `PeopleChooser` and `PeoplePicker` have a listbox which employ two-way data binding.
Both listbox are bound to a following data structure `SelectedAccounts` which is an `ObservableCollection` of type `AccountList`

```c#
public class SelectedAccounts : ObservableCollection<AccountList>
{
    public SelectedAccounts(): base()
    {         
    }
}

public class AccountList : INotifyPropertyChanged
{
    private string _accountName;
    private string _displayName;       
}

```

The below XAML shows the two way databinding with this data structure

```xml
 <ListBox x:Name="UsersListBox" DataContext="selectedAccounts" ItemsSource="{Binding SelectedAccounts, Mode=TwoWay}" HorizontalAlignment="Left" Height="100" Margin="26,43,0,0" VerticalAlignment="Top" Width="182">
    <ListBox.RenderTransform>
        <CompositeTransform SkewX="0.661" TranslateX="0.606"/>
    </ListBox.RenderTransform>
    <ListBox.ItemTemplate>
        <DataTemplate>
            <StackPanel Orientation="Horizontal">
                <TextBlock Text="{Binding DisplayName}"/>
            </StackPanel>
        </DataTemplate>
    </ListBox.ItemTemplate>
</ListBox>
```


`SelectedAccounts` data structure is populated using People WebService.

```c#
PeopleSoapClient ps = new PeopleSoapClient();
ps.Endpoint.Address =
new System.ServiceModel.EndpointAddress(siteUrl + peopleWsUrl);

ps.SearchPrincipalsCompleted += new EventHandler<SearchPrincipalsCompletedEventArgs>(ps_SearchPrincipalsCompleted);

ps.SearchPrincipalsAsync(SearchTxt.Text, 50, SPPrincipalType.User);
```

				
Depending upon if multiple selection is allowed or not, `ListBox` is hidden and `TextBox` is shown instead along with a resolve button.

```c#
public bool AllowMultiple { get; set; }

void PeopleChooser_Loaded(object sender, RoutedEventArgs e)
{
	if (AllowMultiple)
	{
		UsersListBox.Visibility = System.Windows.Visibility.Visible;
		UserTextBox.Visibility = System.Windows.Visibility.Collapsed;
		ResolveButton.Visibility = Visibility.Collapsed;
	}
	else
	{
		UsersListBox.Visibility = System.Windows.Visibility.Collapsed;
		UserTextBox.Visibility = System.Windows.Visibility.Visible;
		ResolveButton.Visibility = Visibility.Visible;
	}

	peoplePicker.AllowMultiple = AllowMultiple;

}
```

If there are muliple results, right mouse button on `TextBox` is handled and displays choices to user to enable him to select a single result.

```c#
private void UserTextBox_MouseRightButtonUp(object sender, MouseButtonEventArgs e)
{
    // Display a menu on mouse right button up
    cMenu = new ContextMenu();
    
    foreach (PickerEntry pi in values.Values)
    {
        mnuItem = new MenuItem();
        mnuItem.Header = pi.DisplayName;
        mnuItem.Name = pi.AccountName;
        mnuItem.Click += mnuItem_Click;
        cMenu.Items.Add(mnuItem);

	}

    cMenu.IsOpen = true;
}

void mnuItem_Click(object sender, RoutedEventArgs e)
{
    MenuItem mnu = sender as MenuItem;

    values = new Dictionary<string, PickerEntry>();
    values.Add(mnu.Name, new PickerEntry(mnu.Header.ToString(), mnu.Name, string.Empty, string.Empty));

    SetSingleResult(values);
}
```
