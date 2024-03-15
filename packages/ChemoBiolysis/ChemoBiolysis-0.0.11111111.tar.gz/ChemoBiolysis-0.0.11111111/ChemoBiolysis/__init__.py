def get_target_values_meanings(y):
    unique_values = y.unique()
    meanings = {}
    for val in unique_values:
        meaning = input(f"Enter the meaning of '{val}': ")
        meanings[val] = meaning
    return meanings

def qsar_assay_fingerprint_analysis(aid_input):
    def retrieve_active_inactive_cids_with_fingerprints_and_pcfp(aid):
        url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/{aid}/cids/txt?cids_type=active'

        # Fetch active CIDs
        response = requests.get(url)
        active_cids = set(map(int, response.text.strip().split()))

        # Create DataFrame
        df1 = pd.DataFrame(list(active_cids), columns=['CID'])
        df1['Activity'] = 'Active'
        url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/{aid}/cids/txt?cids_type=inactive'

        # Fetch active CIDs
        response = requests.get(url)
        active_cids = set(map(int, response.text.strip().split()))

        # Create DataFrame
        df2 = pd.DataFrame(list(active_cids), columns=['CID'])
        df2['Activity'] = 'Inactive'
        # Combine df1 and df2 into a single DataFrame
        df = pd.concat([df1, df2], ignore_index=True)
        display(df)

        # Retrieve fingerprints and PCFP for each CID
        for cid in df['CID']:
            fingerprint_url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/Fingerprint2D/txt'
            fingerprint_response = requests.get(fingerprint_url)
            fingerprint = fingerprint_response.text.strip()

            # Add fingerprint to the DataFrame
            df.loc[df['CID'] == cid, 'Fingerprint2D'] = fingerprint

            # Decode base64 fingerprint and extract PCFP bitstring
            pcfp_bitstring = PCFP_BitString(fingerprint)

            # Add PCFP bitstring columns to the DataFrame
            pcfp_columns = [f'PubchemFP{i}' for i in range(len(pcfp_bitstring))]
            df.loc[df['CID'] == cid, pcfp_columns] = list(pcfp_bitstring)

        return df

    result_df = retrieve_active_inactive_cids_with_fingerprints_and_pcfp(aid_input)
    result_df = result_df.drop(['CID', 'Fingerprint2D'], axis=1)
    # Encode the 'Activity' column
    le_activity = LabelEncoder()
    result_df['Activity'] = le_activity.fit_transform(result_df['Activity'])
    result_df = result_df.astype(int)
    display(result_df)
    X=result_df.drop('Activity', axis=1)
    y=result_df['Activity']
    # Get target values meanings
    target_meanings = get_target_values_meanings(y)

 # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(result_df.drop('Activity', axis=1),result_df['Activity'], test_size=0.2, random_state=2)

    # LazyClassifier
    clf = LazyClassifier(verbose=0, ignore_warnings=True, custom_metric=None, predictions=True)
    models, _ = clf.fit(X_train, X_test, y_train, y_test)

    # Plot the model accuracies
    plt.figure(figsize=(5, 10))
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(y=models.index, x="Accuracy", data=models, palette='viridis')
    ax.set(xlim=(0, 1))
    plt.show()

    # RandomForestClassifier
    clf_rf = RandomForestClassifier(n_estimators=500, random_state=1)
    clf_rf.fit(X_train, y_train)
    y_pred_class_rf = clf_rf.predict(X_test)

    # XGBClassifier
    xgbc = XGBClassifier()
    xgbc.fit(X_train, y_train)
    y_pred_class_xgb = xgbc.predict(X_test)

    # Cross-validation scores
    scores_rf = cross_val_score(clf_rf, X_train, y_train, cv=5)
    print("Random Forest Mean cross-validation score: %.2f" % scores_rf.mean())

    kfold = KFold(n_splits=10, shuffle=True)
    kf_cv_scores_xgb = cross_val_score(xgbc, X_train, y_train, cv=kfold)
    print("XGBClassifier K-fold CV average score: %.2f" % kf_cv_scores_xgb.mean())

    # Feature Importance with Random Forest
    importance_rf = clf_rf.feature_importances_
    feature_names = X.columns
    fp_rf = sorted(range(len(importance_rf)), key=lambda i: importance_rf[i], reverse=True)[:20]
    imp_values_rf = sorted(importance_rf, reverse=True)[:20]

    feature_names_rf = [feature_names[i] for i in fp_rf]
    imp_values_rf

    fake_rf = pd.DataFrame({'ind': feature_names_rf, 'importance__': imp_values_rf})

    # Plot Feature Importance
    sns.set_color_codes("pastel")
    ax_rf = sns.barplot(x='ind', y='importance__', data=fake_rf)
    ax_rf.set(xlabel='Features', ylabel='importance')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

    clf = RandomForestClassifier(n_estimators=500, random_state=1)
    clf.fit(X_train, y_train)
    y_pred_class = clf.predict(X_test)

    cf_matrix = confusion_matrix(y_test, y_pred_class)

    # Plot confusion matrix with target values meanings as titles
    sns.heatmap(cf_matrix, annot=True, cmap='Blues', xticklabels=list(target_meanings.values()), yticklabels=list(target_meanings.values()))
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.show()

    print(classification_report(y_test, y_pred_class))
    return


    #aid_input = input("Enter the AID: ")
#qsar_assay_fingerprint_analysis("1000")
